"""Manage DCOS services

Usage:
    dcos service --info
    dcos service [--inactive --json]
    dcos service log [--follow --lines=N --ssh-config-file=<path>]
                     <service> [<file>]
    dcos service shutdown <service-id>

Options:
    -h, --help                  Show this screen

    --info                      Show a short description of this subcommand

    --ssh-config-file=<path>    Path to SSH config file.  Used to access
                                marathon logs.

    --follow                    Output data as the file grows

    --inactive                  Show inactive services in addition to active
                                ones. Inactive services are those that have
                                been disconnected from master, but haven't yet
                                reached their failover timeout.

    --json                      Print json-formatted services

    --lines=N                   Output the last N lines [default: 10]

    --version                   Show version

Positional Arguments:
    <file>                      Output this file. [default: stdout]

    <service>                   The DCOS Service name.

    <service-id>                The DCOS Service ID
"""

import subprocess

import dcoscli
import docopt
from dcos import cmds, emitting, marathon, mesos, package, util
from dcos.errors import DCOSException
from dcoscli import log, tables

logger = util.get_logger(__name__)
emitter = emitting.FlatEmitter()


def main():
    try:
        return _main()
    except DCOSException as e:
        emitter.publish(e)
        return 1


def _main():
    util.configure_logger_from_environ()

    args = docopt.docopt(
        __doc__,
        version="dcos-service version {}".format(dcoscli.version))

    return cmds.execute(_cmds(), args)


def _cmds():
    """
    :returns: All of the supported commands
    :rtype: [Command]
    """

    return [

        cmds.Command(
            hierarchy=['service', 'log'],
            arg_keys=['--follow', '--lines', '--ssh-config-file', '<service>',
                      '<file>'],
            function=_log),

        cmds.Command(
            hierarchy=['service', 'shutdown'],
            arg_keys=['<service-id>'],
            function=_shutdown),

        cmds.Command(
            hierarchy=['service', '--info'],
            arg_keys=[],
            function=_info),

        cmds.Command(
            hierarchy=['service'],
            arg_keys=['--inactive', '--json'],
            function=_service),
    ]


def _info():
    """Print services cli information.

    :returns: process return code
    :rtype: int
    """

    emitter.publish(__doc__.split('\n')[0])
    return 0


# TODO (mgummelt): support listing completed services as well.
# blocked on framework shutdown.
def _service(inactive, is_json):
    """List dcos services

    :param inactive: If True, include completed tasks
    :type inactive: bool
    :param is_json: If true, output json.
        Otherwise, output a human readable table.
    :type is_json: bool
    :returns: process return code
    :rtype: int
    """

    services = mesos.get_master().frameworks(inactive=inactive)

    if is_json:
        emitter.publish([service.dict() for service in services])
    else:
        table = tables.service_table(services)
        output = str(table)
        if output:
            emitter.publish(output)

    return 0


def _shutdown(service_id):
    """Shuts down a service

    :param service_id: the id for the service
    :type service_id: str
    :returns: process return code
    :rtype: int
    """

    mesos.DCOSClient().shutdown_framework(service_id)
    return 0


def _log(follow, lines, ssh_config_file, service, file_):
    """Prints the contents of the logs for a given service.  The service
    task is located by first identifying the marathon app running a
    framework named `service`.

    :param follow: same as unix tail's -f
    :type follow: bool
    :param lines: number of lines to print
    :type lines: int
    :param ssh_config_file: SSH config file.  Used for marathon.
    :type ssh_config_file: str | None
    :param service: service name
    :type service: str
    :param file_: file path to read
    :type file_: str
    :returns: process return code
    :rtype: int
    """

    lines = util.parse_int(lines)

    if service == 'marathon':
        if file_:
            raise DCOSException('The <file> argument is invalid for marathon.'
                                ' The systemd journal is always used for the'
                                ' marathon log.')

        return _log_marathon(follow, lines, ssh_config_file)
    else:
        if ssh_config_file:
            raise DCOSException(
                'The `--ssh-config-file` argument is invalid for non-marathon '
                'services. SSH is not used.')
        return _log_service(follow, lines, service, file_)


def _log_service(follow, lines, service, file_):
    """Prints the contents of the logs for a given service.  Used for
    non-marathon services.

    :param follow: same as unix tail's -f
    :type follow: bool
    :param lines: number of lines to print
    :type lines: int
    :param service: service name
    :type service: str
    :param file_: file path to read
    :type file_: str
    :returns: process return code
    :rtype: int
    """

    if file_ is None:
        file_ = 'stdout'

    task = _get_service_task(service)
    return _log_task(task['id'], follow, lines, file_)


def _log_task(task_id, follow, lines, file_):
    """Prints the contents of the logs for a given task ID.

    :param task_id: task ID
    :type task_id: str
    :param follow: same as unix tail's -f
    :type follow: bool
    :param lines: number of lines to print
    :type lines: int
    :param file_: file path to read
    :type file_: str
    :returns: process return code
    :rtype: int
    """

    dcos_client = mesos.DCOSClient()
    task = mesos.get_master(dcos_client).task(task_id)
    mesos_file = mesos.MesosFile(file_, task=task, dcos_client=dcos_client)
    return log.log_files([mesos_file], follow, lines)


def _get_service_task(service_name):
    """Gets the task running the given service.  If there is more than one
    such task, throws an exception.

    :param service_name: service name
    :type service_name: str
    :returns: The marathon task dict
    :rtype: dict
    """

    marathon_client = marathon.create_client()
    app = _get_service_app(marathon_client, service_name)
    tasks = marathon_client.get_app(app['id'])['tasks']
    if len(tasks) != 1:
        raise DCOSException(
            ('We expected marathon app [{}] to be running 1 task, but we ' +
             'instead found {} tasks').format(app['id'], len(tasks)))
    return tasks[0]


def _get_service_app(marathon_client, service_name):
    """Gets the marathon app running the given service.  If there is not
    exactly one such app, throws an exception.

    :param marathon_client: marathon client
    :type marathon_client: marathon.Client
    :param service_name: service name
    :type service_name: str
    :returns: marathon app
    :rtype: dict
    """

    apps = package.get_apps_for_framework(service_name, marathon_client)

    if len(apps) > 1:
        raise DCOSException(
            'Multiple marathon apps found for service name [{}]: {}'.format(
                service_name,
                ', '.join('[{}]'.format(app['id']) for app in apps)))
    elif len(apps) == 0:
        raise DCOSException(
            'No marathon apps found for service [{}]'.format(service_name))
    else:
        return apps[0]


def _log_marathon(follow, lines, ssh_config_file):
    """Prints the contents of the marathon logs.

    :param follow: same as unix tail's -f
    :type follow: bool
    :param lines: number of lines to print
    :type lines: int
    :param ssh_config_file: SSH config file.
    :type ssh_config_file: str | None
    ;:returns: process return code
    :rtype: int
    """

    ssh_options = util.get_ssh_options(ssh_config_file, [])

    journalctl_args = ''
    if follow:
        journalctl_args += '-f '
    if lines:
        journalctl_args += '-n {} '.format(lines)

    leader_ip = marathon.create_client().get_leader().split(':')[0]

    cmd = ("ssh {0} core@{1} " +
           "journalctl {2} -u marathon").format(
               ssh_options,
               leader_ip,
               journalctl_args)

    return subprocess.call(cmd, shell=True)

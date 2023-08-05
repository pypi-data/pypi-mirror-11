import sys
from getpass import getuser
from os import getenv, path, SEEK_END
from raven import Client
from subprocess import Popen, PIPE, call
from tempfile import TemporaryFile
from argparse import ArgumentParser, REMAINDER
from sys import argv
from time import time
from .version import VERSION

MAX_MESSAGE_SIZE = 1000

parser = ArgumentParser(
    description='Wraps commands and reports those that fail to Sentry.',
    epilog=('The Sentry server address can also be specified through ' +
            'the SENTRY_DSN environment variable ' +
            '(and the --dsn option can be omitted).'),
    usage='cron-sentry [-h] [--dsn SENTRY_DSN] [--string-max-length STRING_MAX_LENGTH] [--version] cmd [arg ...]',
)
parser.add_argument(
    '--dsn',
    metavar='SENTRY_DSN',
    default=getenv('SENTRY_DSN'),
    help='Sentry server address',
)
parser.add_argument(
    '--string-max-length',
    type=int,
    help='The maximum characters of a string that should be sent to Sentry (use -1 to send all characters)',
)
parser.add_argument(
    '--version',
    action='version',
    version=VERSION,
)
parser.add_argument(
    'cmd',
    nargs=REMAINDER,
    help='The command to run',
)

def update_dsn(opts):
    """Update the Sentry DSN stored in local configs

    It's assumed that the file contains a DSN endpoint like this:
    https://public_key:secret_key@app.getsentry.com/project_id

    It could easily be extended to override all settings if there
    were more use cases.
    """

    homedir = path.expanduser('~%s' % getuser())
    home_conf_file = path.join(homedir, '.cron-sentry')
    system_conf_file = '/etc/cron-sentry.conf'

    conf_precedence = [home_conf_file, system_conf_file]
    for conf_file in conf_precedence:
        if path.exists(conf_file):
            with open(conf_file, "r") as conf:
                opts.dsn = conf.read().rstrip()
            return

def run(args=argv[1:]):
    opts = parser.parse_args(args)

    # Command line takes precendence, otherwise check for local configs
    if not opts.dsn:
        update_dsn(opts)

    if opts.cmd:
        # make cron-sentry work with both approaches:
        #
        #     cron-sentry --dsn http://dsn -- command --arg1 value1
        #     cron-sentry --dsn http://dsn command --arg1 value1
        #
        # see more details at https://github.com/Yipit/cron-sentry/pull/6
        if opts.cmd[0] == '--':
            cmd = opts.cmd[1:]
        else:
            cmd = opts.cmd
        runner = CommandReporter(cmd=cmd, dsn=opts.dsn, string_max_length=opts.string_max_length)
        sys.exit(runner.run())
    else:
        sys.stderr.write("ERROR: Missing command parameter!\n")
        parser.print_usage()
        sys.exit(1)


class CommandReporter(object):
    def __init__(self, cmd, dsn, string_max_length=None):
        self.dsn = dsn
        self.command = cmd
        self.string_max_length = string_max_length

    def run(self):
        start = time()

        with TemporaryFile() as stdout:
            with TemporaryFile() as stderr:
                exit_status = call(self.command, stdout=stdout, stderr=stderr)

                last_lines_stdout = self._get_last_lines(stdout)
                last_lines_stderr = self._get_last_lines(stderr)

                if exit_status > 0:
                    elapsed = int((time() - start) * 1000)
                    self.report_fail(exit_status, last_lines_stdout, last_lines_stderr, elapsed)

                sys.stdout.write(last_lines_stdout)
                sys.stderr.write(last_lines_stderr)
                return exit_status

    def report_fail(self, exit_status, last_lines_stdout, last_lines_stderr, elapsed):
        if self.dsn is None:
            return

        message = "Command \"%s\" failed" % (self.command,)

        client = Client(dsn=self.dsn, string_max_length=self.string_max_length)

        client.captureMessage(
            message,
            data={
                'logger': 'cron',
            },
            extra={
                'command': self.command,
                'exit_status': exit_status,
                'last_lines_stdout': last_lines_stdout,
                'last_lines_stderr': last_lines_stderr,
            },
            time_spent=elapsed
        )

    def _get_last_lines(self, buf):
        buf.seek(0, SEEK_END)
        file_size = buf.tell()
        if file_size < MAX_MESSAGE_SIZE:
            buf.seek(0)
            last_lines = buf.read().decode('utf-8')
        else:
            buf.seek(-(MAX_MESSAGE_SIZE-3), SEEK_END)
            last_lines = u'...' + buf.read().decode('utf-8')
        return last_lines

from db_facts.runner import Runner
import unittest
from io import StringIO
from unittest.mock import patch
from db_facts.errors import UserErrorException


@patch('db_facts.runner.db')
@patch('sys.stderr', new_callable=StringIO)
@patch('sys.stdout', new_callable=StringIO)
class TestRunner(unittest.TestCase):
    maxDiff = None

    def test_runner_no_arg(self,
                           mock_stdout,
                           mock_stderr,
                           mock_db):
        runner = Runner()
        with self.assertRaises(SystemExit):
            runner.run(['/bin/db-facts'])
        self.assertIn('the following arguments are required: dbname',
                      mock_stderr.getvalue())
        self.assertEqual(mock_stdout.getvalue(), '')

    def test_runner_too_many_args(self,
                                  mock_stdout,
                                  mock_stderr,
                                  mock_db):
        runner = Runner()
        out = runner.run(['/bin/db-facts', '--config', '--json', 'foo'])
        self.assertEqual(out, 1)
        self.assertIn('Please specify only one of --json or --config',
                      mock_stderr.getvalue())
        self.assertEqual(mock_stdout.getvalue(), '')

    def test_runner_exception(self,
                              mock_stdout,
                              mock_stderr,
                              mock_db):
        runner = Runner()
        mock_db.side_effect = UserErrorException('error message here')

        self.assertEqual(1, runner.run(['/bin/db-facts', 'foo']))
        mock_db.assert_called_with(['foo'])
        self.assertEqual(mock_stderr.getvalue(), 'error message here\n')
        self.assertEqual(mock_stdout.getvalue(), '')

    def test_runner_help(self,
                         mock_stdout,
                         mock_stderr,
                         mock_db):
        runner = Runner()
        with self.assertRaises(SystemExit):
            runner.run(['/bin/db-facts', '--help'])
        self.assertEqual(mock_stderr.getvalue(), '')
        helpstr = ('usage: db-facts [-h] [--json] [--config] dbname\n'
                   '\n'
                   'Pull information about databases from '
                   'user-friendly names\n'
                   '\n'
                   'positional arguments:\n'
                   '  dbname      Friendly name of database '
                   '(e.g., "redshift", "dnc", "cms-impl-\n'
                   '              dbadmin")\n'
                   '\n'
                   'optional arguments:\n'
                   '  -h, --help  show this help message and exit\n'
                   '  --json      Report output in JSON format '
                   '(default: env vars)\n'
                   '  --config    Report output in db-facts config '
                   'format (default: env vars)\n')

        def without_whitespace(s: str) -> str:
            return s.replace(" ", "").replace("\n", "")

        self.assertEqual(without_whitespace(mock_stdout.getvalue()),
                         without_whitespace(helpstr))

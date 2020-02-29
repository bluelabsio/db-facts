from db_facts.runner import Runner
import unittest
from io import StringIO
from unittest.mock import patch
from db_facts.errors import UserErrorException


def without_whitespace(s: str) -> str:
    return s.replace(" ", "").replace("\n", "")


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
        out = runner.run(['/bin/db-facts'])
        self.assertEqual(out, 1)
        self.assertIn(without_whitespace('Pull information about databases from'),
                      without_whitespace(mock_stderr.getvalue()))
        self.assertEqual(mock_stdout.getvalue(), '')

    def test_runner_exception(self,
                              mock_stdout,
                              mock_stderr,
                              mock_db):
        runner = Runner()
        mock_db.side_effect = UserErrorException('error message here')

        self.assertEqual(1, runner.run(['/bin/db-facts', 'sh', 'foo']))
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
        helpstr = """
usage: db-facts [-h] {list,json,config,sh} ...

Pull information about databases from user-friendly names

positional arguments:
  {list,json,config,sh}
    list                List available dbnames
    json                Report output in JSON format
    config              Report output in db-facts config format
    sh                  Report output in Bourne shell envionment variable format

optional arguments:
  -h, --help            show this help message and exit"""

        self.assertEqual(without_whitespace(mock_stdout.getvalue()),
                         without_whitespace(helpstr))

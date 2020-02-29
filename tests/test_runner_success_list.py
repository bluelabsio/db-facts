from db_facts.runner import Runner
import unittest
from io import StringIO
from unittest.mock import patch


@patch('sys.stderr', new_callable=StringIO)
@patch('sys.stdout', new_callable=StringIO)
class TestRunnerList(unittest.TestCase):

    @patch('db_facts.list_db_names.load_config')
    def test_runner_list(self,
                         mock_load_config,
                         mock_stdout,
                         mock_stderr):
        runner = Runner()
        mock_load_config.return_value = {
            'dbs': {
                'mydb1': {
                    'description': 'My favorite database',
                    'password': 'password',
                    'host': 'host',
                    'user': 'user',
                    'type': 'type',
                    'protocol': 'protocol',
                    'port': 123,
                    'database': 'dbname',
                    'lastpass_share_name_suffix': 'lastpass_share_name_suffix',
                    'connection_type': 'connection_type',
                },
                'mydb2': {
                    'password': 'password',
                    'host': 'host',
                    'user': 'user',
                    'type': 'type',
                    'protocol': 'protocol',
                    'port': 123,
                    'database': 'dbname',
                    'lastpass_share_name_suffix': 'lastpass_share_name_suffix',
                    'connection_type': 'connection_type',
                }
            }
        }

        self.assertEqual(0, runner.run(['/bin/db-facts', 'list']))
        mock_load_config.assert_called_with()
        self.assertEqual(mock_stderr.getvalue(), '')
        self.assertEqual(mock_stdout.getvalue(),
                         ("Available db_names:\n"
                          "* mydb1 (My favorite database)\n"
                          "* mydb2\n"))

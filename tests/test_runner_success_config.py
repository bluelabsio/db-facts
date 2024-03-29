from db_facts.runner import Runner
import unittest
from io import StringIO
from unittest.mock import patch
import yaml


@patch('db_facts.runner.db')
@patch('sys.stderr', new_callable=StringIO)
@patch('sys.stdout', new_callable=StringIO)
class TestRunnerSuccessConfig(unittest.TestCase):

    def test_runner_lpass_config(self,
                                 mock_stdout,
                                 mock_stderr,
                                 mock_db):
        runner = Runner()
        mock_db.return_value = {
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

        self.assertEqual(0, runner.run(['/bin/db-facts', 'config', 'foo']))
        mock_db.assert_called_with(['foo'])
        self.assertEqual(mock_stderr.getvalue(), '')
        parsed_yaml_value = {
            'dbs': {
                'foo': {
                    'exports': {
                        'database': 'dbname',
                        'user': 'user',
                        'password': 'password',
                        'port': 123,
                        'protocol': 'protocol',
                        'type': 'type',
                        'host': 'host',
                        'lastpass_share_name_suffix': 'lastpass_share_name_suffix',
                        'connection_type': 'connection_type'
                    }
                }
            }
        }
        self.assertEqual(yaml.safe_load(mock_stdout.getvalue()),
                         parsed_yaml_value)

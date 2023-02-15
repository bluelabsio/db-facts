from db_facts.runner import Runner
import unittest
from io import StringIO
from unittest.mock import patch


@patch('db_facts.runner.db')
@patch('sys.stderr', new_callable=StringIO)
@patch('sys.stdout', new_callable=StringIO)
class TestRunner(unittest.TestCase):
    def test_runner_lpass(self,
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
            'not-valid*_characters1': 'whatever',
            'connection_type': 'connection_type',
        }

        self.assertEqual(0, runner.run(['/bin/db-facts', 'sh', 'foo']))
        mock_db.assert_called_with(['foo'])
        self.assertEqual(mock_stderr.getvalue(), '')
        self.assertEqual(mock_stdout.getvalue(),
                         'export CONNECTION_TYPE\n'
                         'CONNECTION_TYPE=connection_type\n'
                         'export DB_DATABASE\n'
                         'DB_DATABASE=dbname\n'
                         'export DB_HOST\n'
                         'DB_HOST=host\n'
                         'export LASTPASS_SHARE_NAME_SUFFIX\n'
                         'LASTPASS_SHARE_NAME_SUFFIX='
                         'lastpass_share_name_suffix\n'
                         'export NOTVALID_CHARACTERS1\n'
                         'NOTVALID_CHARACTERS1=whatever\n'
                         'export DB_PASSWORD\n'
                         'DB_PASSWORD=password\n'
                         'export DB_PORT\n'
                         'DB_PORT=123\n'
                         'export DB_PROTOCOL\n'
                         'DB_PROTOCOL=protocol\n'
                         'export DB_TYPE\n'
                         'DB_TYPE=type\n'
                         'export DB_USERNAME\n'
                         'DB_USERNAME=user\n')

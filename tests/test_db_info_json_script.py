from db_facts.db_info import db
import unittest
from unittest.mock import patch
from .mock_dbcli_config import mock_dbcli_config


@patch('db_facts.db_info.pull_jinja_context')
@patch('db_facts.db_info.subprocess')
class TestDBInfoJsonScript(unittest.TestCase):
    def test_db_info_json_script(self,
                                 mock_subprocess,
                                 mock_pull_jinja_context):

        expected_result = {
            'a': 'b',
            'c': 'd',
            'connection_type': 'direct',
        }
        mock_subprocess.check_output.return_value = b'{"a": "b", "c": "d"}'
        mock_pull_jinja_context.return_value = ({}, {})
        db_facts = db(['baz'], dbcli_config=mock_dbcli_config)
        self.assertEqual(expected_result, db_facts)
        mock_pull_jinja_context.\
            assert_called_with(['baz'],
                               mock_dbcli_config['dbs']['baz'],
                               mock_dbcli_config)
        mock_subprocess.check_output.\
            assert_called_with(['some-custom-json-script'])

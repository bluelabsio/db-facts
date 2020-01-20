from db_facts.db_info import db
import unittest
from unittest.mock import patch
from .mock_dbcli_config import mock_dbcli_config


@patch('db_facts.db_info.pull_jinja_context')
@patch('db_facts.db_info.db_info_from_lpass')
@patch('db_facts.lpass.lpass_field')
class TestDBInfoLastPass(unittest.TestCase):
    def test_db_info_lastpass(self,
                              mock_lpass_field,
                              mock_db_info_from_lpass,
                              mock_pull_jinja_context):

        expected_result = {
            'database': 'database',
            'host': 'host',
            'password': 'password',
            'port': 'port',
            'protocol': 'protocol',
            'type': 'type',
            'user': 'user',
            'connection_type': 'direct'
        }
        mock_db_info_from_lpass.return_value = {
            'password': 'password',
            'host': 'host',
            'user': 'user',
            'type': 'type',
            'protocol': 'protocol',
            'port': 'port',
            'database': 'database',
        }
        mock_pull_jinja_context.return_value = ({}, {})
        db_facts = db(['bazzle'], dbcli_config=mock_dbcli_config)
        mock_db_info_from_lpass.assert_called_with('lpass entry name')
        self.assertEqual(expected_result, db_facts)
        mock_pull_jinja_context.\
            assert_called_with(['bazzle'],
                               mock_dbcli_config['dbs']['bazzle'],
                               mock_dbcli_config)

    def test_db_info_pull_lastpass_user_and_pass_only(self,
                                                      mock_lpass_field,
                                                      mock_db_info_from_lpass,
                                                      mock_pull_jinja_context):

        lpass_entry = {
            'username': 'user',
            'password': 'password',
        }

        def fake_lpass_field(entry_name, field_name):
            assert entry_name == 'lpass entry name'
            return lpass_entry[field_name]
        mock_lpass_field.side_effect = fake_lpass_field
        expected_result = {
            'password': 'password',
            'user': 'user',
            'connection_type': 'direct',
            'some_additional': 'export',
            'a_numbered_export': 123,
        }
        mock_pull_jinja_context.return_value = ({}, {})
        db_facts = db(['frink'], dbcli_config=mock_dbcli_config)
        mock_lpass_field.assert_called_with('lpass entry name', 'password')
        self.assertEqual(expected_result, db_facts)
        mock_pull_jinja_context.\
            assert_called_with(['frink'],
                               mock_dbcli_config['dbs']['frink'],
                               mock_dbcli_config)

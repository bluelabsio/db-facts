from db_facts.db_info import db
import unittest
from unittest.mock import patch
from .mock_dbcli_config import mock_dbcli_config


@patch('db_facts.db_info.pull_jinja_context')
@patch('db_facts.db_info.db_info_from_lpass')
@patch('db_facts.lpass.lpass_field')
class TestDBInfo(unittest.TestCase):
    def test_db_info_two_level_with_config(self,
                                           mock_lpass_field,
                                           mock_db_info_from_lpass,
                                           mock_pull_jinja_context):

        self.maxDiff = True

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
        mock_jinja_context = {}
        mock_filters = {}
        mock_pull_jinja_context.return_value = (mock_jinja_context,
                                                mock_filters)
        db_facts = db(['bazzle', 'bing'], dbcli_config=mock_dbcli_config)

        self.assertEqual(expected_result, db_facts)
        mock_pull_jinja_context.\
            assert_called_with(['bazzle', 'bing'],
                               mock_dbcli_config['dbs']['bazzle-bing'],
                               mock_dbcli_config)

    def test_db_info_two_level_with_one_level_config(self,
                                                     mock_lpass_field,
                                                     mock_db_info_from_lpass,
                                                     mock_pull_jinja_context):

        self.maxDiff = None

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
        db_facts = db(['frazzle', 'mumble'], dbcli_config=mock_dbcli_config)
        self.assertEqual(expected_result, db_facts)
        mock_pull_jinja_context.\
            assert_called_with(['frazzle', 'mumble'],
                               mock_dbcli_config['dbs']['frazzle'],
                               mock_dbcli_config)

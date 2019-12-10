from db_facts.db_info import db
from db_facts.errors import UserErrorException
import unittest
from unittest.mock import patch
from .mock_dbcli_config import mock_dbcli_config


@patch('db_facts.db_info.pull_jinja_context')
@patch('db_facts.db_info.subprocess')
class TestDBInfoErrors(unittest.TestCase):
    def test_db_info_bad_db(self,
                            mock_subprocess,
                            mock_pull_jinja_context):
        mock_pull_jinja_context.return_value = ({}, {})
        with self.assertRaises(UserErrorException):
            db(['not-there'], dbcli_config=mock_dbcli_config)

    def test_db_info_invalid_db_connect_method(self,
                                               mock_subprocess,
                                               mock_pull_jinja_context):
        mock_pull_jinja_context.return_value = ({}, {})
        with self.assertRaises(SyntaxError):
            db(['bing'], dbcli_config=mock_dbcli_config)

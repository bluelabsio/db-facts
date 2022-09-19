from db_facts.db_info import db
import unittest
from unittest.mock import patch
from .mock_dbcli_config import mock_dbcli_config


@patch("db_facts.db_info.pull_jinja_context")
@patch("db_facts.db_info.db_info_from_secrets_manager")
@patch("db_facts.aws_secrets_manager.pull_aws_secrets_manager_secret")
class TestDBInfoSecretsManager(unittest.TestCase):
    def test_db_info_secrets_manager(
        self,
        mock_pull_aws_secrets_manager_secret,
        mock_db_info_from_secrets_manager,
        mock_pull_jinja_context,
    ):

        expected_result = {
            "database": "database",
            "host": "host",
            "password": "password",
            "port": "port",
            "protocol": "protocol",
            "type": "type",
            "user": "user",
            "connection_type": "direct",
        }
        mock_db_info_from_secrets_manager.return_value = {
            "database": "database",
            "port": "port",
            "host": "host",
            "type": "type",
            "user": "user",
            "protocol": "protocol",
            "password": "password",
        }
        mock_pull_jinja_context.return_value = ({}, {})
        db_facts = db(["fromage"], dbcli_config=mock_dbcli_config)
        mock_db_info_from_secrets_manager.assert_called_with(
            "secrets manager entry name"
        )
        self.assertEqual(expected_result, db_facts)
        mock_pull_jinja_context.assert_called_with(
            ["fromage"], mock_dbcli_config["dbs"]["fromage"], mock_dbcli_config
        )

    def test_db_info_pull_secrets_manager_user_and_pass_only(
        self,
        mock_pull_aws_secrets_manager_secret,
        mock_db_info_from_secrets_manager,
        mock_pull_jinja_context,
    ):

        sm_entry = {
            "username": "user",
            "password": "password",
        }

        mock_pull_aws_secrets_manager_secret.return_value = sm_entry
        expected_result = {
            "password": "password",
            "user": "user",
            "connection_type": "direct",
            "some_additional": "export",
            "a_numbered_export": 123,
        }
        mock_pull_jinja_context.return_value = ({}, {})
        db_facts = db(["fronk"], dbcli_config=mock_dbcli_config)
        mock_pull_aws_secrets_manager_secret.assert_called_with(
            "secrets manager entry name"
        )
        self.assertEqual(expected_result, db_facts)
        mock_pull_jinja_context.assert_called_with(
            ["fronk"], mock_dbcli_config["dbs"]["fronk"], mock_dbcli_config
        )

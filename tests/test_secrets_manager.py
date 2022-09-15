import unittest
from unittest.mock import patch

from db_facts import aws_secrets_manager


class TestSecretsManager(unittest.TestCase):
    @patch("db_facts.aws_secrets_manager.pull_aws_secrets_manager_secret")
    def test_db_info_from_secrets_manager(self, mock_pull_from_aws_sm):
        mock_pull_from_aws_sm.return_value = {
            "Database": "fakedatabase",
            "Port": 123,
            "Hostname": "fakehost",
            "Type": "faketype",
            "Username": "fakeuser",
            "Password": "fakepassword",
        }
        db_info = aws_secrets_manager.db_info_from_secrets_manager("my_secret")
        expected_db_info = {
            "database": "fakedatabase",
            "host": "fakehost",
            "password": "fakepassword",
            "port": 123,
            "type": "faketype",
            "user": "fakeuser",
            "protocol": "faketype",  # if we don't know, just pass through
        }

        assert db_info == expected_db_info

from db_facts.jinja_context import pull_jinja_context
import unittest
from unittest.mock import patch
from .mock_dbcli_config import mock_dbcli_config


@patch('db_facts.env_jinja_context.os')
class TestEnvJinjaContext(unittest.TestCase):
    def test_with_env_set(self, mock_os):
        config = {
            'jinja_context_name': 'env',
        }
        context, filters = pull_jinja_context(['whatever', 'whatever'], config, mock_dbcli_config)
        self.assertEqual(context['getenv'], mock_os.getenv)

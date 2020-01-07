from db_facts.jinja_context import pull_jinja_context
import unittest
from unittest.mock import patch
from .mock_dbcli_config import mock_dbcli_config


@patch('db_facts.util.subprocess')
class TestNilJinjaContext(unittest.TestCase):
    def test_nil_context(self, mock_subprocess):
        config = {}
        context, filters = pull_jinja_context(['notthere', 'alsonotthere'],
                                              config, mock_dbcli_config)
        self.assertEquals(context, {})

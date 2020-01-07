from db_facts.jinja_context import pull_jinja_context
import unittest
from unittest.mock import patch
from .mock_dbcli_config import mock_dbcli_config


@patch('db_facts.util.subprocess')
class TestMultiJinjaContext(unittest.TestCase):
    def test_multi(self, mock_subprocess):
        config = {
            'jinja_context_name': [
                'env',
                'base64',
            ]
        }
        mock_subprocess.check_output.return_value = b'username'
        context, filters = pull_jinja_context(['gaggle'], config, mock_dbcli_config)
        decode = filters['b64decode']
        encode = filters['b64encode']
        self.assertEqual(decode(encode('foo')), 'foo')

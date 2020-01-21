import unittest
from unittest.mock import patch, Mock
from db_facts.jinja_context import get_context_pullers
import db_facts


@patch('db_facts.jinja_context.pkg_resources')
class TestJinjaContext(unittest.TestCase):
    def setUp(self):
        db_facts.jinja_context._context_pullers = None

    def test_get_context_pullers_no_plugins(self,
                                            mock_pkg_resources):
        mock_pkg_resources.iter_entry_points.return_value = []
        pullers = get_context_pullers()
        self.assertEqual(list(pullers.keys()), ['env', 'base64'])
        mock_pkg_resources.iter_entry_points.assert_called_with('db_facts.jinja_contexts')

    def test_get_context_pullers_with_one_plugin(self,
                                                 mock_pkg_resources):
        mock_pkg_resources.iter_entry_points.return_value = [
        ]
        mock_mumble_puller = Mock(name='mumble_puller')
        mock_mumble_module = Mock(name='mumble_module')
        mock_mumble_module.name = 'mumble'
        mock_mumble_module.load.return_value = mock_mumble_puller
        mock_pkg_resources.iter_entry_points.return_value = [
            mock_mumble_module
        ]
        pullers = get_context_pullers()
        self.assertEqual(list(pullers.keys()), ['env', 'base64', 'mumble'])
        self.assertEqual(pullers['mumble'], mock_mumble_puller)

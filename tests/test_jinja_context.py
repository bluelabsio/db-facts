import unittest
from unittest.mock import patch, Mock
from db_facts.jinja_context import get_context_pullers
import db_facts


@patch('db_facts.jinja_context.getattr')
@patch('db_facts.jinja_context.importlib')
@patch('db_facts.jinja_context.pkgutil')
class TestJinjaContext(unittest.TestCase):
    def setUp(self):
        db_facts.jinja_context._context_pullers = None

    def test_get_context_pullers_no_plugins(self,
                                            mock_pkgutil,
                                            mock_importlib,
                                            mock_getattr):
        mock_db_facts_finder = Mock(name='db_facts_finder')
        mock_pkgutil.iter_modules.return_value = [
            (mock_db_facts_finder, 'db_facts', True)
        ]
        pullers = get_context_pullers()
        self.assertEqual(list(pullers.keys()), ['env', 'base64'])

    def test_get_context_pullers_with_one_plugin(self,
                                                 mock_pkgutil,
                                                 mock_importlib,
                                                 mock_getattr):
        mock_db_facts_finder = Mock(name='db_facts_finder')
        mock_db_facts_mumble_finder = Mock(name='db_facts_mumble_finder')
        mock_db_facts_mumble_module = mock_importlib.import_module.return_value
        mock_somethingelse_finder = Mock(name='somethingelse_finder')
        mock_getattr.return_value = {'mumble': Mock(name='mumble_puller')}
        mock_pkgutil.iter_modules.return_value = [
            (mock_db_facts_finder, 'db_facts', True),
            (mock_db_facts_mumble_finder, 'db_facts_mumble', True),
            (mock_somethingelse_finder, 'somethingelse', True),
        ]
        pullers = get_context_pullers()
        mock_importlib.import_module.assert_called_with('db_facts_mumble')
        mock_getattr.assert_called_with(mock_db_facts_mumble_module, 'context_pullers', None)
        self.assertEqual(list(pullers.keys()), ['env', 'base64', 'mumble'])

    def test_get_context_pullers_with_one_plugin_but_no_config(self,
                                                               mock_pkgutil,
                                                               mock_importlib,
                                                               mock_getattr):
        mock_db_facts_finder = Mock(name='db_facts_finder')
        mock_db_facts_mumble_finder = Mock(name='db_facts_mumble_finder')
        mock_db_facts_mumble_module = mock_importlib.import_module.return_value
        mock_somethingelse_finder = Mock(name='somethingelse_finder')
        mock_getattr.return_value = None
        mock_pkgutil.iter_modules.return_value = [
            (mock_db_facts_finder, 'db_facts', True),
            (mock_db_facts_mumble_finder, 'db_facts_mumble', True),
            (mock_somethingelse_finder, 'somethingelse', True),
        ]
        pullers = get_context_pullers()
        mock_importlib.import_module.assert_called_with('db_facts_mumble')
        mock_getattr.assert_called_with(mock_db_facts_mumble_module, 'context_pullers', None)
        self.assertEqual(list(pullers.keys()), ['env', 'base64'])

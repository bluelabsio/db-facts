import unittest
from unittest.mock import patch, Mock
from db_facts.jinja_context import get_context_pullers
import db_facts


class TestJinjaContext(unittest.TestCase):
    def setUp(self):
        db_facts.jinja_context._context_pullers = None

    def tearDown(self):
        db_facts.jinja_context._context_pullers = None

    @patch('db_facts.jinja_context.pkg_resources')
    def test_get_context_pullers(self, mock_pkg_resources):
        mock_entry_point_a = Mock(name='entry_point_a')
        mock_pkg_resources.iter_entry_points.return_value = [mock_entry_point_a]
        pullers = get_context_pullers()
        self.assertEqual(pullers, {
            mock_entry_point_a.name:
            mock_entry_point_a.load.return_value
        })

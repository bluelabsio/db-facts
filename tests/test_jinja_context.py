import unittest
from db_facts.jinja_context import get_context_pullers
import db_facts


class TestJinjaContext(unittest.TestCase):
    def setUp(self):
        db_facts.jinja_context._context_pullers = None

    def test_get_context_pullers(self):
        pullers = get_context_pullers()
        self.assertEqual(set(pullers.keys()), {'env', 'base64'})

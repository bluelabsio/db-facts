# ************************************************
# *** ATTENTION *** THIS DOES NOT USE LASTPASS ***
# ************************************************
# BlueLabs is currently transitioning off lastpass and onto 1password.
# Even though this file says "lpass", all underlying calls to the
# lpass CLI have been replaced with calls to the 1password CLI.

import unittest
from unittest.mock import patch
from db_facts import lpass


class TestLPass(unittest.TestCase):
    def test_lpass_field_url_raises(self):
        with self.assertRaises(NotImplementedError):
            lpass.lpass_field('my_name', 'url')

    def test_lpass_field_notes_raises(self):
        with self.assertRaises(NotImplementedError):
            lpass.lpass_field('my_name', 'notes')

    @patch('db_facts.lpass.check_output')
    def test_lpass_field_username(self, mock_check_output):
        mock_check_output.return_value = "fakeuser\n".encode("utf-8")
        out = lpass.lpass_field('my_name', 'username')
        mock_check_output.assert_called_with(
            ['op', 'item', 'get', 'my_name', '--field', 'label=username'])
        assert out == "fakeuser"

    @patch('db_facts.lpass.check_output')
    def test_lpass_field_password(self, mock_check_output):
        mock_check_output.return_value = "fakepassword\n".encode("utf-8")
        out = lpass.lpass_field('my_name', 'password')
        mock_check_output.assert_called_with(
            ['op', 'item', 'get', 'my_name', '--field', 'label=password'])
        assert out == "fakepassword"

    @patch('db_facts.lpass.check_output')
    def test_lpass_field_field1(self, mock_check_output):
        mock_check_output.return_value = "fakefield1\n".encode("utf-8")
        out = lpass.lpass_field('my_name', 'field1')
        mock_check_output.assert_called_with(
            ['op', 'item', 'get', 'my_name', '--field', 'label=field1'])
        assert out == "fakefield1"

    @patch('db_facts.lpass.check_output')
    def test_db_info_from_lpass(self, mock_check_output):
        def fake_check_output(args):
            assert args[0] == 'op'
            assert args[1] == 'item'
            assert args[2] == 'get'
            assert args[3] == 'my_lpass_name'
            assert args[4] == '--field'
            ret = {
                "label=username": 'fakeuser',
                "label=password": 'fakepassword',
                "label=Hostname": 'fakehost',
                "label=Port": '123',
                "label=Type": 'faketype',
                "label=Database": 'fakedatabase',
            }
            return (ret[args[5]] + "\n").encode('utf-8')
        mock_check_output.side_effect = fake_check_output
        db_info = lpass.db_info_from_lpass('my_lpass_name')
        expected_db_info = {
            'database': 'fakedatabase',
            'host': 'fakehost',
            'password': 'fakepassword',
            'port': 123,
            'type': 'faketype',
            'user': 'fakeuser',
            'protocol': 'faketype',  # if we don't know, just pass through
        }
        assert db_info == expected_db_info

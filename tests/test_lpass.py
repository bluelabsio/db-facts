# ************************************************
# *** ATTENTION *** THIS DOES NOT USE LASTPASS ***
# ************************************************
# BlueLabs is currently transitioning off lastpass and onto 1password.
# Even though this file says "lpass", all underlying calls to the
# lpass CLI have been replaced with calls to the 1password CLI.

import json
import unittest
from subprocess import CalledProcessError
from unittest.mock import patch
from db_facts import lpass


class TestLPass(unittest.TestCase):
    def test_lpass_field_url_raises(self):
        with self.assertRaises(NotImplementedError):
            lpass.lpass_field('my_name', 'url')

    @patch('db_facts.lpass.check_output', side_effect=CalledProcessError(1, "mocked_op"))
    def test_lpass_error_with_underlying_process(self, mock_check_output):
        with self.assertRaises(CalledProcessError):
            lpass.lpass_field('my_name', 'field1')

    @patch('db_facts.lpass.check_output')
    def test_lpass_bad_json_from_process(self, mock_check_output):
        return_json = "{"
        mock_check_output.return_value = return_json
        with self.assertRaises(json.JSONDecodeError):
            lpass.lpass_field('my_name', 'field1')

    @patch('db_facts.lpass.check_output')
    def test_lpass_field_notes_uses_notesPlain(self, mock_check_output):
        notes_json = json.dumps({'field': 'are you sick of json.dumps yet'})
        return_json = {
            'id': 'notesPlain',
            'value': notes_json,
        }
        mock_check_output.return_value = json.dumps(return_json).encode('utf-8')
        out = lpass.lpass_field('my_name', 'notes')
        mock_check_output.assert_called_with(
            ['op', 'item', 'get', 'my_name', '--field', 'label=notesPlain', '--format=json'])
        assert out == notes_json

    @patch('db_facts.lpass.check_output')
    def test_lpass_field_username(self, mock_check_output):
        return_json = {
            'id': 'username',
            'value': 'fakeuser'
        }
        mock_check_output.return_value = json.dumps(return_json).encode('utf-8')
        out = lpass.lpass_field('my_name', 'username')
        mock_check_output.assert_called_with(
            ['op', 'item', 'get', 'my_name', '--field', 'label=username', '--format=json'])
        assert out == "fakeuser"

    @patch('db_facts.lpass.check_output')
    def test_lpass_field_password(self, mock_check_output):
        return_json = {
            'id': 'password',
            'value': 'fakepassword',
        }
        mock_check_output.return_value = json.dumps(return_json).encode('utf-8')
        out = lpass.lpass_field('my_name', 'password')
        mock_check_output.assert_called_with(
            ['op', 'item', 'get', 'my_name', '--field', 'label=password', '--format=json'])
        assert out == "fakepassword"

    @patch('db_facts.lpass.check_output')
    def test_lpass_field_field1(self, mock_check_output):
        return_json = {
            'id': 'field1',
            'value': 'fakefield1',
        }
        mock_check_output.return_value = json.dumps(return_json).encode('utf-8')
        out = lpass.lpass_field('my_name', 'field1')
        mock_check_output.assert_called_with(
            ['op', 'item', 'get', 'my_name', '--field', 'label=field1', '--format=json'])
        assert out == "fakefield1"

    @patch('db_facts.lpass.check_output')
    def test_db_info_from_lpass(self, mock_check_output):
        def fake_check_output(args):
            assert args[0] == 'op'
            assert args[1] == 'item'
            assert args[2] == 'get'
            assert args[3] == 'my_lpass_name'
            assert args[4] == '--field'
            assert args[6] == '--format=json'
            ret = {
                "label=username": {'value': 'fakeuser'},
                "label=password": {'value': 'fakepassword'},
                "label=Hostname": {'value': 'fakehost'},
                "label=Port": {'value': '123'},
                "label=Type": {'value': 'faketype'},
                "label=Database": {'value': 'fakedatabase'},
            }
            return json.dumps(ret[args[5]]).encode('utf-8')

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

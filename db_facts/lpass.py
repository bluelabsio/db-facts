import sys
from subprocess import check_output
from .db_facts_types import LastPassUsernamePassword
from .db_type import canonicalize_db_type, db_protocol
import re
import logging
import json



def pull_lastpass_username_password(lastpass_entry_name: str) -> LastPassUsernamePassword:
    return {
        'user': lpass_field(lastpass_entry_name, 'username'),
        'password': lpass_field(lastpass_entry_name, 'password'),
    }


"""
Takes a lastpass secret_id and translates it to the 
"""
def translate_secret_id_to_sm(secret_id: str) -> str:
    cms_secret_pattern = r'(CMS Vertica) (\([a-z]+\)): ([a-z]+)'
    cms_secret_pattern = re.compile(cms_secret_pattern)
    if cms_secret_pattern.match(secret_id):
        match = re.search(cms_secret_pattern, secret_id)
        stack = match.group(2).replace('(', '').replace(')', '')
        username = match.group(3)
        secretsmanager_secret_id = f'{stack}_vertica_{username}_creds'
    else:
        raise NotImplementedError("Currently only CMS secret IDs can be translated to secretsmanager")
    return secretsmanager_secret_id


def lpass_field(name: str, field: str) -> str:
    if field == 'notes':
        field_arg = '--notes'
    elif field == 'username':
        field_arg = '--username'
    elif field == 'password':
        field_arg = '--password'
    elif field == 'url':
        field_arg = '--url'
    else:
        field_arg = '--field=' + field
    raw_output = check_output(['lpass',
                               'show',
                               field_arg,
                               name])
    return raw_output.decode('utf-8').rstrip('\n')


def sm_field(name: str, field: str) -> str:
    sm_name = translate_secret_id_to_sm(name)
    show_command = ["aws", "secretsmanager", "get-secret-value", "--secret-id", sm_name, "--output", "json"]
    raw_output = check_output(show_command)
    decoded_output = raw_output.decode('utf-8').rstrip('\n')
    json_output = json.loads(decoded_output)
    secret_string_json = json.loads(json_output['SecretString'])
    sm_field = secret_string_json[field]
    return sm_field


def db_info_from_lpass(lpass_entry_name: str):
    user = lpass_field(lpass_entry_name, 'username')
    password = lpass_field(lpass_entry_name, 'password')
    host = lpass_field(lpass_entry_name, 'Hostname')
    port = int(lpass_field(lpass_entry_name, 'Port'))
    raw_db_type = lpass_field(lpass_entry_name, 'Type')
    db_type = canonicalize_db_type(raw_db_type)
    dbname = lpass_field(lpass_entry_name, 'Database')

    return {'password': password,
            'host': host,
            'user': user,
            'type': db_type,
            'protocol': db_protocol(db_type),
            'port': port,
            'database': dbname}


def db_info_from_secretsmanager(sm_entry_name: str):
    user = sm_field(sm_entry_name, 'Username')
    password = sm_field(sm_entry_name, 'Password')
    host = sm_field(sm_entry_name, 'Hostname')
    port = int(sm_field(sm_entry_name, 'Port'))
    raw_db_type = sm_field(sm_entry_name, 'Type')
    db_type = canonicalize_db_type(raw_db_type)
    dbname = sm_field(sm_entry_name, 'Database')

    return {'password': password,
            'host': host,
            'user': user,
            'type': db_type,
            'protocol': db_protocol(db_type),
            'port': port,
            'database': dbname}

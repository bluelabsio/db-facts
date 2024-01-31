# ************************************************
# *** ATTENTION *** THIS DOES NOT USE LASTPASS ***
# ************************************************
# BlueLabs is currently transitioning off lastpass and onto 1password.
# Even though this file says "lpass", all underlying calls to the
# lpass CLI have been replaced with calls to the 1password CLI.

import json
from subprocess import check_output, CalledProcessError
from .db_facts_types import LastPassUsernamePassword, LastPassAWSIAM
from .db_type import canonicalize_db_type, db_protocol
import logging


def pull_lastpass_username_password(lastpass_entry_name: str) -> LastPassUsernamePassword:
    return {
        'user': lpass_field(lastpass_entry_name, 'username'),
        'password': lpass_field(lastpass_entry_name, 'password'),
    }


def pull_lastpass_aws_iam(lastpass_entry_name: str) -> LastPassAWSIAM:
    result = pull_lastpass_username_password(lastpass_entry_name)
    return {
        'aws_access_key_id': result['user'],
        'aws_secret_access_key': result['password']
    }


def lpass_field(name: str, field: str) -> str:
    # *** ATTENTION *** THIS DOES NOT USE LASTPASS ***

    # This used to use the lastpass-cli to pull credentials. But we've moved
    # from lastpass to 1password. This command retrieves the fields in the
    # same format from 1password instead.

    # Note this won't work for URLs, which 1password stores
    # different from lpass. But as of now db-facts doesn't ever rely on
    # this field.
    if field == 'url':
        raise NotImplementedError(
            'Cannot retrieve URL field from 1password')

    # The field lastpass stored notes in was called "notes", but the field
    # 1password stores notes in is called "notesPlain".
    if field == 'notes':
        field = 'notesPlain'

    log = logging.getLogger(__name__)
    try:
        raw_output = check_output(
            ['op', 'item', 'get', name, '--field', f'label={field}', '--format=json'])
        parsed_output = json.loads(raw_output)
        return parsed_output['value']
    except (CalledProcessError, KeyError):
        log.error(
            f'Error from 1password CLI retrieving {field} from "{name}".\n' +
            'Do you have the 1password CLI installed?\n' +
            f'Does the entry {name} exist in your 1password account?\n' +
            f'Does this entry have the field: {field}?')
        raise


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

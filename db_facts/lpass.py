from subprocess import check_output
from .db_facts_types import LastPassUsernamePassword, LastPassAWSIAM
from .db_type import canonicalize_db_type, db_protocol


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
    # This used to use the lastpass-cli to pull credentials. But we've moved
    # from lastpass to 1password. This command retrieves the fields in the
    # same format from 1password instead.

    # Note this won't work for the way 1password stores notes and URLs, which
    # is different from lpass. But as of now db-facts doesn't ever rely on
    # these fields.
    raw_output = check_output(
        ['op', 'item', 'get', name, '--field', f'label={field}'])

    return raw_output.decode('utf-8').rstrip('\n')


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

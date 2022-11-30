import subprocess
import json
from .template import template, template_any
from .jinja_context import pull_jinja_context
from .errors import fail_on_invalid_db_name
from .config import load_config
from .lpass import pull_lastpass_username_password, db_info_from_lpass, pull_lastpass_aws_iam
from .aws_secrets_manager import (
    db_info_from_secrets_manager,
    pull_aws_secrets_manager_username_password
)
from .db_facts_types import DBConfig, DBCLIConfig, DBFacts, DBName
from .db_config import db_config


def db(db_name: DBName, dbcli_config: DBCLIConfig = None) -> DBFacts:
    """Get connection info for specified database.

    :param db_name: Alias for the particular database endpoint and account to connect to.  ['a','b','c'] corresponds to 'a-b-c' on the db-facts command-line.
    :raises UserErrorException: Raised if db_name cannot be found.
    """

    if dbcli_config is None:
        dbcli_config = load_config()

    config = db_config(dbcli_config, db_name)
    if config is None:
        fail_on_invalid_db_name(db_name)

    exports_from = config.get('exports_from')
    db_info: DBConfig = {
        'exports': {
            'connection_type': 'direct',
        }
    }
    if exports_from is not None:
        db_info['exports_from'] = exports_from

    jinja_context = pull_jinja_context(db_name, config, dbcli_config)
    for k in config.keys():
        if k == 'jinja_context_name':
            pass
        elif k == 'exports':
            db_info['exports'].update({
                template(exportname,
                         jinja_context): template_any(config['exports'][exportname], jinja_context)
                for exportname in config['exports']
            })
        else:
            db_info[k] = template(config[k], jinja_context)

    if 'exports_from' in db_info:
        method = db_info.get('exports_from')
        if method is None:
            # nothing to do here - all the info we need is already in
            # dbcli.yml, either fixed or interpolated through the
            # jinja context
            pass
        if 'json_script' in dbcli_config['exports_from'][method]:
            json_call_args = \
                dbcli_config['exports_from'][method]['json_script']
            json_call =\
                [template(s, (db_info, {})) for s in json_call_args]
            json_str = subprocess.check_output(json_call).decode('utf-8')
            additional_attributes = json.loads(json_str)
            db_info['exports'].update(additional_attributes)
        elif 'pull_lastpass_from' in dbcli_config['exports_from'][method]:
            template_for_lastpass_entry_name =\
                dbcli_config['exports_from'][method]['pull_lastpass_from']
            lastpass_entry_name = template(template_for_lastpass_entry_name,
                                           (db_info, {}))
            additional_attributes = \
                db_info_from_lpass(lastpass_entry_name)
            db_info['exports'].update(additional_attributes)
        elif 'pull_lastpass_username_password_from' in \
             dbcli_config['exports_from'][method]:
            method = dbcli_config['exports_from'][method]
            template_for_lastpass_entry_name =\
                method['pull_lastpass_username_password_from']
            lastpass_entry_name = template(template_for_lastpass_entry_name,
                                           (db_info, {}))
            additional_attributes = \
                pull_lastpass_username_password(lastpass_entry_name)
            db_info['exports'].update(additional_attributes)
        elif 'pull_lastpass_aws_iam' in dbcli_config['exports_from'][method]:
            method = dbcli_config['exports_from'][method]
            template_for_lastpass_entry_name =\
                method['pull_lastpass_aws_iam']
            lastpass_entry_name = template(template_for_lastpass_entry_name,
                                           (db_info, {}))
            additional_attributes = \
                pull_lastpass_aws_iam(lastpass_entry_name)
            db_info['exports'].update(additional_attributes)
        elif 'pull_secrets_manager_from' in dbcli_config['exports_from'][method]:
            template_for_secrets_manager_entry_name =\
                dbcli_config['exports_from'][method]['pull_secrets_manager_from']
            secrets_manager_entry_name = template(template_for_secrets_manager_entry_name,
                                                  (db_info, {}))
            additional_attributes = \
                db_info_from_secrets_manager(secrets_manager_entry_name)
            db_info['exports'].update(additional_attributes)
        elif 'pull_secrets_manager_username_password_from' in \
             dbcli_config['exports_from'][method]:
            method = dbcli_config['exports_from'][method]
            template_for_secrets_manager_entry_name =\
                method['pull_secrets_manager_username_password_from']
            secrets_manager_entry_name = template(template_for_secrets_manager_entry_name,
                                           (db_info, {}))
            additional_attributes = \
                pull_aws_secrets_manager_username_password(secrets_manager_entry_name)
            db_info['exports'].update(additional_attributes)
        else:
            raise SyntaxError(f'Did not understand exports_from {method}')

    return db_info['exports']

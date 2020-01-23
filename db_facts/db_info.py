import subprocess
import json
from .template import template, template_any
from .jinja_context import pull_jinja_context
from .errors import fail_on_invalid_db_name
from .config import load_config
from .lpass import pull_lastpass_username_password, db_info_from_lpass
from .db_facts_types import DBConfig, DBCLIConfig, DBFacts, DBName
from .db_config import db_config


def db(db_name: DBName, dbcli_config: DBCLIConfig = None) -> DBFacts:
    """Get connection info for specified database."""

    if dbcli_config is None:
        dbcli_config = load_config()

    config = db_config(dbcli_config, db_name)
    if config is None:
        fail_on_invalid_db_name(db_name)

    db_connect_method = config.get('db_connect_method')
    db_info: DBConfig = {
        'exports': {
            'connection_type': 'direct',
        }
    }
    if db_connect_method is not None:
        db_info['db_connect_method'] = db_connect_method

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

    if 'db_connect_method' in db_info:
        method = db_info.get('db_connect_method')
        if method is None:
            # nothing to do here - all the info we need is already in
            # dbcli.yml, either fixed or interpolated through the
            # jinja context
            pass
        if 'json_script' in dbcli_config['db_connect_method'][method]:
            json_call_args = \
                dbcli_config['db_connect_method'][method]['json_script']
            json_call =\
                [template(s, (db_info, {})) for s in json_call_args]
            json_str = subprocess.check_output(json_call).decode('utf-8')
            additional_attributes = json.loads(json_str)
            db_info['exports'].update(additional_attributes)
        elif 'pull_lastpass_from' in dbcli_config['db_connect_method'][method]:
            template_for_lastpass_entry_name =\
                dbcli_config['db_connect_method'][method]['pull_lastpass_from']
            lastpass_entry_name = template(template_for_lastpass_entry_name,
                                           (db_info, {}))
            additional_attributes = \
                db_info_from_lpass(lastpass_entry_name)
            db_info['exports'].update(additional_attributes)
        elif 'pull_lastpass_username_password_from' in \
             dbcli_config['db_connect_method'][method]:
            method = dbcli_config['db_connect_method'][method]
            template_for_lastpass_entry_name =\
                method['pull_lastpass_username_password_from']
            lastpass_entry_name = template(template_for_lastpass_entry_name,
                                           (db_info, {}))
            additional_attributes = \
                pull_lastpass_username_password(lastpass_entry_name)
            db_info['exports'].update(additional_attributes)
        else:
            raise SyntaxError(f'Did not understand db_connect_method {method}')

    return db_info['exports']

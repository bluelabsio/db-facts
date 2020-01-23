from .db_facts_types import DBConfig, DBCLIConfig, DBName
from typing import Optional


def db_config(dbcli_config: DBCLIConfig, db_name: DBName) -> Optional[DBConfig]:
    dbs = dbcli_config['dbs']

    config_name = "-".join(db_name)

    if config_name in dbs:
        return dbs[config_name]

    if len(db_name) <= 1:
        return None

    # try again without the last component - Sometimes we want the
    # second and third parts of a db_name to be parsed dynamically by
    # the jinja context functions, and sometimes that's overkill and
    # we can just specify the config for specific two- or three- entry
    # db_names.
    return db_config(dbcli_config, db_name[0:-1])

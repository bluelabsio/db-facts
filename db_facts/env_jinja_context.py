import os
from .db_facts_types import JinjaContext, DBName, DBCLIConfig


def pull_env_jinja_context(db_name: DBName, dbcli_config: DBCLIConfig) -> JinjaContext:
    return {
        # Returns None if key not found unless default specified
        'getenv': os.getenv,
        # Raises if key not found
        'env': lambda key: os.environ[key],
    }

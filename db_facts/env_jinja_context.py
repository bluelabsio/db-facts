import os
from .db_facts_types import JinjaContext, DBName, DBCLIConfig


def pull_env_jinja_context(db_name: DBName, dbcli_config: DBCLIConfig) -> JinjaContext:
    """Returns a Jinja context that exports the following functions:

    * getenv(key: str, default: Optional[str]=None) -> Optional[str]:
      Return the value of the environment variable key if it exists,
      or default if it doesn’t. key, default and the result are str.
    * env(key: str) -> str: Looks up an environment variable value, or
      raises KeyError if not found.
    """
    return {
        # Returns None if key not found unless default specified
        'getenv': os.getenv,
        # Raises if key not found
        'env': lambda key: os.environ[key],
    }

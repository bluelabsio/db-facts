import os


def pull_env_jinja_context(db_name, dbcli_config):
    return {
        # Returns None if key not found unless default specified
        'getenv': os.getenv,
        # Raises if key not found
        'env': lambda key: os.environ[key],
    }

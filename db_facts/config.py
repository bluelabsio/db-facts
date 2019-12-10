import logging
from pathlib import Path
import os
from os.path import expanduser
import yaml


logger = logging.getLogger(__name__)

# Prefixes to scan for config files (from lowest priority to highest priority)
CONFIG_PREFIXES = ['/etc', '/usr/local/etc', '~', '.']


def merge_configs(*configs):
    """
    Merges dictionaries of dictionaries, by combining top-level dictionaries with last value taking
    precedence.

    For example:
    >>> merge_configs({'a': {'b': 1, 'c': 2}}, {'a': {'b': 2, 'd': 3}})
    {'a': {'b': 2, 'c': 2, 'd': 3}}
    """
    merged_config = {}
    for config in configs:
        for k, v in config.items():
            if k in merged_config:
                merged_config[k].update(v)
            else:
                merged_config[k] = v.copy()
    return merged_config


def enumerate_configs(config_prefix, file_prefix):
    return (config_prefix / f'{file_prefix}dbfacts.d').glob('*')


def find_configs():
    config_paths_to_load = []
    for config_prefix in map(lambda p: Path(expanduser(p)), CONFIG_PREFIXES):
        if config_prefix in [Path.home(), Path('.')]:
            file_prefix = '.'
        else:
            file_prefix = ''

        config_paths_to_load.append(config_prefix / f'{file_prefix}dbfacts.yml')
        config_paths_to_load.extend(enumerate_configs(config_prefix, file_prefix))
    if 'DB_FACTS_PATH' in os.environ:
        paths = [
            Path(expanduser(rawpath))
            for rawpath in os.environ['DB_FACTS_PATH'].split(':')
        ]
        config_paths_to_load.extend(reversed(paths))

    return [path for path in config_paths_to_load if path.is_file()]


def load_config(config_paths_to_load=None):
    loaded_configs = []
    if config_paths_to_load is None:
        config_paths_to_load = find_configs()

    for config_path in config_paths_to_load:
        path = Path(config_path)
        logger.info('Merging db facts config from %s', config_path)
        with path.open('r') as configfile:
            config = yaml.safe_load(configfile)
            if isinstance(config, dict):
                loaded_configs.append(config)
            else:
                logger.warning('Config %s appears to be invalid', config_path)

    return merge_configs(*loaded_configs)

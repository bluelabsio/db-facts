from pathlib import Path
from nose.tools import eq_
from db_facts.config import merge_configs, load_config


def test_merge_configs():
    result = merge_configs(
        {'a': {'b': 1, 'c': 2}},
        {'a': {'b': 2, 'd': 3}, 'e': {'f': 'g'}},
        {'e': {'f': 'h'}},
    )

    eq_(result, {
        'a': {'b': 2, 'c': 2, 'd': 3},
        'e': {'f': 'h'},
    })


def test_load_config():
    """Tests that defaults are preserved if override files don't include an override."""

    config = load_config(config_paths_to_load=[Path(__file__).parent / 'files' / 'test.yml'])
    eq_('blah', config['dbs']['newconfig']['exports']['host'])


def test_load_config_no_paths():
    """Tests that can disable default config."""
    config = load_config(config_paths_to_load=[])
    eq_(config, {})

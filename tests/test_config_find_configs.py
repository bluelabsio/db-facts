from pathlib import Path
from unittest.mock import patch
from nose.tools import eq_
from db_facts.config import find_configs


def fake_enumerate_configs(config_prefix, file_prefix):
    if config_prefix == Path('/etc'):
        return [config_prefix / f'{file_prefix}dbfacts.d' / '001_fake.yml']
    elif config_prefix == Path('/usr/local/etc'):
        return [config_prefix / f'{file_prefix}dbfacts.d' / '002_fake.yml']
    elif config_prefix == Path.home():
        return [config_prefix / f'{file_prefix}dbfacts.d' / '003_fake.yml']
    elif config_prefix == Path('.'):
        return [config_prefix / f'{file_prefix}dbfacts.d' / '004_fake.yml']
    else:
        return []


@patch('db_facts.config.enumerate_configs', new=fake_enumerate_configs)
@patch('db_facts.config.Path.is_file')
def test_find_configs(mock_is_file):
    mock_is_file.return_value = True
    eq_(find_configs(), [
        Path('/etc/dbfacts.yml'),
        Path('/etc/dbfacts.d/001_fake.yml'),
        Path('/usr/local/etc/dbfacts.yml'),
        Path('/usr/local/etc/dbfacts.d/002_fake.yml'),
        Path.home() / '.dbfacts.yml',
        Path.home() / '.dbfacts.d/003_fake.yml',
        Path('.dbfacts.yml'),
        Path('.dbfacts.d/004_fake.yml')
    ])


@patch.dict('os.environ', {
    'DB_FACTS_PATH': '/foo/bar/dbfacts.yml:/foo/bar/custom.yml',
})
@patch('db_facts.config.enumerate_configs', new=fake_enumerate_configs)
@patch('db_facts.config.Path.is_file')
def test_find_configs_with_env_var(mock_is_file):
    mock_is_file.return_value = True
    eq_(find_configs(), [
        Path('/etc/dbfacts.yml'),
        Path('/etc/dbfacts.d/001_fake.yml'),
        Path('/usr/local/etc/dbfacts.yml'),
        Path('/usr/local/etc/dbfacts.d/002_fake.yml'),
        Path.home() / '.dbfacts.yml',
        Path.home() / '.dbfacts.d/003_fake.yml',
        Path('.dbfacts.yml'),
        Path('.dbfacts.d/004_fake.yml'),
        Path('/foo/bar/custom.yml'),
        Path('/foo/bar/dbfacts.yml'),
    ])

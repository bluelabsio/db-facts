from typing import NoReturn
from .db_facts_types import DBName


class UserErrorException(Exception):
    pass


def fail_on_invalid_db_name(db_name: DBName) -> NoReturn:
    raise UserErrorException('-'.join(db_name) + ' is not a valid DB name.')

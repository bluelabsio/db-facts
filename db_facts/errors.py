from typing import NoReturn


class UserErrorException(Exception):
    pass


def fail_on_invalid_db_name(db_name: str) -> NoReturn:
    raise UserErrorException('-'.join(db_name) + ' is not a valid DB name.')

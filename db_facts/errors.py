from typing import NoReturn
from .db_facts_types import DBName


class UserErrorException(Exception):
    """
    Raised upon an error related to the inputs to the db() function.
    """
    pass


def fail_on_invalid_db_name(db_name: DBName) -> NoReturn:
    raise UserErrorException('-'.join(db_name) + ' is not a valid DB name.  '
                             'To list valid databases, run "db-facts list" and to configure a '
                             'new database, please see '
                             'https://github.com/bluelabsio/db-facts/blob/master/CONFIGURATION.md')

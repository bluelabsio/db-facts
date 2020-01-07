from __future__ import print_function
import sys
from .db_info import db
from .exports import print_exports
from .errors import UserErrorException
import argparse
import json


class Runner():
    def __init__(self):
        pass

    def run(self, args):
        try:
            desc = 'Pull information about databases from user-friendly names'
            parser = argparse.ArgumentParser(prog='db-facts', description=desc)
            parser.add_argument('--json', dest='json', action='store_const',
                                const=True, default=False,
                                help=('Report output in JSON format '
                                      '(default: env vars)'))
            parser.add_argument('dbname', nargs=1,
                                help=('Friendly name of database '
                                      '(e.g., "redshift", "dnc", '
                                      '"cms-impl-dbadmin")'))

            args = parser.parse_args(args[1:])

            db_name_str = args.dbname[0]
            db_name = db_name_str.split('-')

            db_info = db(db_name)

            if args.json:
                print(json.dumps(db_info, sort_keys=True, indent=4))
            else:
                print_exports(db_info)
            return 0
        except UserErrorException as e:
            print(str(e), file=sys.stderr)
            return 1

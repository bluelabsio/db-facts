from __future__ import print_function
import sys
from .db_info import db
from .exports import print_exports
from .config_yaml import config_yaml
from typing import List
from .errors import UserErrorException
import argparse
import json


class Runner():
    def __init__(self) -> None:
        pass

    def run(self, argv: List[str]) -> int:
        try:
            desc = 'Pull information about databases from user-friendly names'
            parser = argparse.ArgumentParser(prog='db-facts', description=desc)
            parser.add_argument('--json', dest='json', action='store_const',
                                const=True, default=False,
                                help=('Report output in JSON format '
                                      '(default: env vars)'))
            parser.add_argument('--config', dest='config', action='store_const',
                                const=True, default=False,
                                help=('Report output in db-facts config format '
                                      '(default: env vars)'))
            parser.add_argument('dbname', nargs=1,
                                help=('Friendly name of database '
                                      '(e.g., "redshift", "dnc", '
                                      '"cms-impl-dbadmin")'))

            args = parser.parse_args(argv[1:])

            db_name_str: str = args.dbname[0]
            db_name = db_name_str.split('-')

            db_info = db(db_name)

            if args.json and args.config:
                print("Please specify only one of --json or --config", file=sys.stderr)
                parser.print_help(file=sys.stderr)
                return 1
            elif args.json:
                print(json.dumps(db_info, sort_keys=True, indent=4))
            elif args.config:
                print(config_yaml(db_name_str, db_info), end='')
            else:
                print_exports(db_info)
            return 0
        except UserErrorException as e:
            print(str(e), file=sys.stderr)
            return 1

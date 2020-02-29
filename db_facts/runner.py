from __future__ import print_function
import sys
from .db_info import db
from .exports import print_exports
from .list_db_names import list_db_names
from .config_yaml import config_yaml
from typing import List
from .errors import UserErrorException
import argparse
import json


class Runner():
    def __init__(self) -> None:
        pass

    def dump_json(self, args: argparse.Namespace) -> None:
        db_name_str: str = args.dbname[0]
        db_name = db_name_str.split('-')

        db_info = db(db_name)

        print(json.dumps(db_info, sort_keys=True, indent=4))

    def dump_config(self, args: argparse.Namespace):
        db_name_str: str = args.dbname[0]
        db_name = db_name_str.split('-')

        db_info = db(db_name)
        print(config_yaml(db_name_str, db_info), end='')

    def dump_sh(self, args: argparse.Namespace):
        db_name_str: str = args.dbname[0]
        db_name = db_name_str.split('-')

        db_info = db(db_name)
        print_exports(db_info)

    def run(self, argv: List[str]) -> int:
        try:
            desc = 'Pull information about databases from user-friendly names'
            parser = argparse.ArgumentParser(prog='db-facts', description=desc)
            subparsers = parser.add_subparsers()

            list_parser = subparsers.add_parser('list', help='List available dbnames')
            list_parser.set_defaults(func=lambda args: list_db_names())

            json_parser = subparsers.add_parser('json', help='Report output in JSON format')
            json_parser.add_argument('dbname', nargs=1,
                                     help=('Friendly name of database '
                                           '(e.g., "redshift", "dmv", '
                                           '"abc-dev-dbadmin")'))
            json_parser.set_defaults(func=self.dump_json)

            config_parser = subparsers.add_parser('config',
                                                  help='Report output in db-facts config format')
            config_parser.add_argument('dbname', nargs=1,
                                       help=('Friendly name of database '
                                             '(e.g., "redshift", "dmv", '
                                             '"abc-dev-dbadmin")'))
            config_parser.set_defaults(func=self.dump_config)

            sh_parser = subparsers.add_parser('sh',
                                              help=('Report output in Bourne shell envionment '
                                                    'variable format '))
            sh_parser.add_argument('dbname', nargs=1,
                                   help=('Friendly name of database '
                                         '(e.g., "redshift", "dmv", '
                                         '"abc-dev-dbadmin")'))
            sh_parser.set_defaults(func=self.dump_sh)

            args = parser.parse_args(argv[1:])
            if 'func' not in args:
                parser.print_help(file=sys.stderr)
                return 1
            args.func(args)

            return 0
        except UserErrorException as e:
            print(str(e), file=sys.stderr)
            return 1

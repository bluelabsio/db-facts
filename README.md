# db-facts

db-facts translates from user-familiar database coordinates (e.g.,
"redshift", "corppostgres dbadmin", "productoracle impl juser") into
detailed instructions on how to access the database in question,
providing configuration and templating mechnisms to wrap any
credential management tools involved in providing those details and
credentials.

Example:

```sh
$ db-facts redshift
export CONNECTION_TYPE
CONNECTION_TYPE=direct
export LASTPASS_SHARE_NAME_SUFFIX
LASTPASS_SHARE_NAME_SUFFIX='blue labs redshift'
export DB_PASSWORD
DB_PASSWORD='hunter2'
DB_HOST=whatevs.whatevs.us-east-1.redshift.amazonaws.com
export DB_HOST
export DB_DATABASE
DB_DATABASE=analytics
export DB_USERNAME
DB_USERNAME=vbroz
export DB_PORT
DB_PORT=5439
export DB_TYPE
DB_TYPE=redshift
export DB_PROTOCOL
DB_PROTOCOL=postgres
```

To do this, it relies on a config file ("dbcli.yml") which teaches it
how to parse the user-friendly coordinates.  Much of the heavy lifting
in the parsing part is done
by
[jinja_context.py](https://github.com/bluelabsio/db-facts/blob/master/db_facts/jinja_context.py),
which sets some variables and functions that can be used in jinja
templates within the config file.

This is part of the suite of programs which allow a user to type in
things like `db redshift` and connect via their own credentials to the
configured database named 'redshift'.  Other parts of this chain can
be found in the [ws-scripts](https://github.com/bluelabsio/ws-scripts)
repo.

If you need to set the instructions immediately to your environment
variables, you can do this with the command:
```sh
eval $(db-facts redshift)
```

## Configuration

You can configure `db-facts` to connect to your databases.  See
[CONFIGURATION.md](./CONFIGURATION.md) for details.

## Extensions

You can extend `db-facts` to pull configuration from other systems.
See [EXTENSIONS.md](./EXTENSIONS.md) for details.

## Library

To use as a library:

```sh
$ python
Python 3.5.2 (default, Sep 12 2016, 09:31:17)
[GCC 4.2.1 Compatible Apple LLVM 7.3.0 (clang-703.0.31)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import bluelabs_db_facts
>>> db_facts.db(['redshift'])
{'protocol': 'postgres', 'lastpass_share_name_suffix': 'blue labs redshift', 'host': 'bl-int-analytics1.cxtyzogmmhiv.us-east-1.redshift.amazonaws.com', 'connection_type': 'direct', 'user': 'vbroz', 'database': 'analytics', 'password': 'hunter1', 'port': 5439, 'type': 'redshift'}
>>>
```

## Development

See [DEVELOPMENT.md](./DEVELOPMENT.md)

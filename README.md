# db-facts

db-facts translates from user-familiar database coordinates (e.g.,
"redshift", "corppostgres dbadmin", "productoracle impl juser") into
detailed instructions on how to access the database in question,
providing configuration and templating mechnisms to wrap any
credential management tools involved in providing those details and
credentials.

Example:

```sh
$ db-facts sh redshift
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

For details on the potential facts returned, see the
[API reference](https://db-facts.readthedocs.io/en/latest/db_facts.html#db_facts.DBFacts).

`db-facts` relies on a config file ("dbcli.yml") which teaches it
how to parse the user-friendly coordinates.  Much of the heavy lifting
in the parsing part is done
by
[jinja_context.py](https://github.com/bluelabsio/db-facts/blob/master/db_facts/jinja_context.py),
which sets some variables and functions that can be used in jinja
templates within the config file.

If you need to set the instructions immediately to your environment
variables, you can do this with the command:
```sh
eval $(db-facts sh redshift)
```

For AWS IAM credentials in Lastpass, ensure that this block exists under
`exports_from:` in your db-facts config:
```
  lpass_aws_iam:
    pull_lastpass_aws_iam: "{{ lastpass_entry }}"
```
and set up a db credential with export_type `lpass_aws_iam`, for example:
```
  aws_user_example:
    exports_from: lpass_aws_iam
    lastpass_entry: 'AWS IAM: example_user'
```
You can then credential your shell with this one-liner:
`eval $(db-facts sh aws_user_example)`

You can also access `db-facts` via a Python API; for details, see the
[API reference](https://db-facts.readthedocs.io/en/latest/db_facts.html#module-db_facts).

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


## Plugins 
Homebrew install db-facts tries to download the config file but pip doesnt have a way of managing this dependency. 
The user has to download and install the config manaully.
- Download the tar file: https://github.com/bluelabsio/bluelabs-db-facts/archive/refs/tags/v6.0.0.tar.gz
- Install the archive: `pip install bluelabs-db-facts-6.0.0.tar.gz`


## Command Documentation 
<b>Summary:</b> Retrieves the database connection properties depending on the format the user specifies.

<b> Valid Database Names:</b> {seiu,redshift,everytown,...}, {seiu,redshift,everytown,...}-dbadmin, {seiu,redshift,everytown, ...}-username, bluehq-{job,cred,user,...}, singularity, cms{-prod,-test,-impl}{-dbadmin,}

Note: If the database if of type CMS the password id and password key is converted from lpastpass to AWS secretsmanager.

- The <b>service account</b> password id in secretsmanager has the naming ocnvention:  `{stack}_vertica_service_accounts`. The password key in secretsmanager has the naming convention: `{user}_password`.
- The personal account database password id in secretsmanager has the naming convention: `{stack}_vertica_{user}_creds`. The password key in secretsmanager has the naming convention: `Password`.

<br>

#### <i>Report output in Bourne shell envionment variable format</i>
<b>Run command:</b> `db-facts sh "[database name]"`

<br>

#### <i>List available dbnames</i>
<b>Run command:</b> `db-facts ls "[database name]"`

<br>

#### <i>Report output in JSON format</i>
<b>Run command:</b> `db-facts json "[database name]"`

<br>

#### <i>Report output in db-facts config format</i>
<b>Run command:</b> `db-facts config "[database name]"`
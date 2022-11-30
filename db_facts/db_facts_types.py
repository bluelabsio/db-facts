from typing import Any, Dict, Callable, Union, Tuple, List, TYPE_CHECKING
# note: this file cannot be named 'types.py' or I encounter IDE heartache:
#
#  https://stackoverflow.com/questions/36669895/site-py-attributeerror-module-object-has-no-attribute-moduletype-upon-runn
#
# 🤷


if TYPE_CHECKING:
    from mypy_extensions import TypedDict

    # Declare this only during type checking, because I don't want to
    # require mypy as a dependency (the types are built into the
    # language, the type checker and its extensions are a separate
    # package).

    # As you encounter needs to add fields below for other types of
    # databases, feel free to PR additions here (or maintain your own
    # type/ignore this one, of course).
    class DBFacts(TypedDict, total=False):
        """This is a dictionary type which describes the output of the db()
        method - a dict of various facts about the database in
        question.  All keys are optional except 'type', and keys
        should only be provided if relevant to the database type.
        """

        user: str
        "Database username"

        password: str
        "Database password"

        host: str
        "Database hostname"

        type: str
        "Database type (canonical examples: postgres, vertica, mysql, redshift, bigquery)"

        protocol: str
        """Database protocol type (often the same value as 'type', but may
        vary for databases like Redshift which offer protocol
        compatibilities with e.g. postgres)"""

        port: int
        "Database port number"

        database: str
        """Database name - this concepts varys quite a bit from database to
        database, but is often used to distinguish between completely
        separate databases that share the same underlying
        infrastructure (e.g., same port and host, but different
        database)."""

        bq_default_project_id: str
        "BigQuery-specific - the project to be used if no specific project is specified"

        bq_default_dataset_id: str
        "BigQuery-specific - the dataset to be used if no specific dataset is specified"

        bq_service_account_json: str
        """BigQuery-specific - JSON (serialized to a string) representing the service account
        credentials to be used."""

else:
    DBFacts = Dict[str, Any]
DBName = List[str]
LastPassUsernamePassword = Dict[str, str]
LastPassAWSIAM = Dict[str, str]
AWSSecret = Any
AWSSecretUsernamePassword = Dict[str, str]
DBConfig = Dict[str, Any]
DBCLIConfig = Any
JinjaContext = Dict[str, Any]
JinjaFilter = Callable[[Any], Any]
JinjaFilters = Dict[str, JinjaFilter]
JinjaContextPuller = Callable[[DBName, DBCLIConfig],
                              Union[JinjaContext, Tuple[JinjaContext, JinjaFilters]]]

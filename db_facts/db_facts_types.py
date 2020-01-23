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
        user: str
        password: str
        host: str
        type: str
        protocol: str
        port: int
        database: str
        bq_default_project_id: str
        bq_default_dataset_id: str
        bq_service_account_json: str
else:
    DBFacts = Dict[str, Any]
DBName = List[str]
LastPassUsernamePassword = Dict[str, str]
DBConfig = Dict[str, Any]
DBCLIConfig = Any
JinjaContext = Dict[str, Any]
JinjaFilter = Callable[[Any], Any]
JinjaFilters = Dict[str, JinjaFilter]
JinjaContextPuller = Callable[[DBName, DBCLIConfig],
                              Union[JinjaContext, Tuple[JinjaContext, JinjaFilters]]]

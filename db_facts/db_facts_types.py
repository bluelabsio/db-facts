from typing import Any, Dict, Callable, Union, Tuple

# note: this file cannot be named 'types.py' or I encounter IDE heartache:
#
#  https://stackoverflow.com/questions/36669895/site-py-attributeerror-module-object-has-no-attribute-moduletype-upon-runn
#
# 🤷

DBName = List[str]
LastPassUsernamePassword = Dict[str, str]
DBConfig = Dict[str, Any]
DBCLIConfig = Any
DBFacts = Dict[str, Any]
JinjaContext = Dict[str, Any]
JinjaFilter = Callable[[Any], Any]
JinjaFilters = Dict[str, JinjaFilter]
JinjaContextPuller = Callable[[DBName, DBCLIConfig],
                              Union[JinjaContext, Tuple[JinjaContext, JinjaFilters]]]

from typing import Any, Dict, Callable

DBName = str
LastPassUsernamePassword = Dict[str, str]
DBConfig = Dict[str, Any]
DBCLIConfig = Any
DBFacts = Dict[str, Any]
JinjaContext = Dict[str, Any]
JinjaFilter = Callable[[Any], Any]
JinjaFilters = Dict[str, JinjaFilter]

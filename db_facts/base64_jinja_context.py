import base64
from .db_facts_types import DBName, DBCLIConfig, JinjaContext, JinjaFilters
from typing import Tuple


def pull_base64_jinja_context(db_name: DBName,
                              dbcli_config: DBCLIConfig) -> Tuple[JinjaContext,
                                                                  JinjaFilters]:
    return ({},
            {
                'b64decode': lambda s: base64.b64decode(s).decode('utf-8'),
                'b64encode': lambda s: base64.b64encode(s.encode('utf-8')).decode('utf-8'),
            })

from .base64_jinja_context import pull_base64_jinja_context
from .env_jinja_context import pull_env_jinja_context
from .types import DBName, DBConfig, DBCLIConfig, JinjaContext, JinjaFilters
from typing import Dict, Callable, Union, Tuple, Optional


context_pullers: Dict[str,
                      Callable[[DBName, DBCLIConfig],
                               Union[JinjaContext,
                                     Tuple[JinjaContext,
                                           JinjaFilters]]]] = {
    'env': pull_env_jinja_context,
    'base64': pull_base64_jinja_context,
}


def pull_jinja_context(db_name: DBName,
                       config: DBConfig,
                       dbcli_config: DBCLIConfig) -> Tuple[JinjaContext, JinjaFilters]:
    if 'jinja_context_name' not in config:
        return ({}, {})
    else:
        all_jinja_context_names = config['jinja_context_name']
        if not isinstance(all_jinja_context_names, list):
            all_jinja_context_names = [all_jinja_context_names]

        full_context: JinjaContext = {}
        full_filters: JinjaFilters = {}
        for jinja_context_name in all_jinja_context_names:
            if jinja_context_name in context_pullers:
                context_or_context_and_filters = \
                    context_pullers[jinja_context_name](db_name, dbcli_config)
                context: JinjaContext
                filters: Optional[JinjaFilters] = None
                if isinstance(context_or_context_and_filters, tuple):
                    context, filters = context_or_context_and_filters
                else:
                    context = context_or_context_and_filters
                full_context.update(context)
                if filters is not None:
                    full_filters.update(filters)
            else:
                raise Exception('Invalid jinja_context_name (' +
                                jinja_context_name + ')')

        return full_context, full_filters

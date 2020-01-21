from .base64_jinja_context import pull_base64_jinja_context
from .env_jinja_context import pull_env_jinja_context
from .db_facts_types import (DBName, DBConfig, DBCLIConfig, JinjaContext, JinjaFilters,
                             JinjaContextPuller)
from typing import Dict, Tuple, Optional
import pkg_resources
import logging


logger = logging.getLogger(__name__)


_context_pullers: Optional[Dict[str, JinjaContextPuller]] = None


def get_context_pullers() -> Dict[str, JinjaContextPuller]:
    global _context_pullers

    if _context_pullers is not None:
        return _context_pullers

    _context_pullers = {
        'env': pull_env_jinja_context,
        'base64': pull_base64_jinja_context,
    }

    # https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins
    # https://packaging.python.org/guides/creating-and-discovering-plugins/#using-naming-convention
    discovered_pullers = {
        entry_point.name: entry_point.load()
        for entry_point
        in pkg_resources.iter_entry_points('db_facts.jinja_contexts')
    }
    _context_pullers.update(discovered_pullers)

    return _context_pullers


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
            pullers = get_context_pullers()
            if jinja_context_name in pullers:
                context_or_context_and_filters = \
                    pullers[jinja_context_name](db_name, dbcli_config)
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

from .base64_jinja_context import pull_base64_jinja_context
from .env_jinja_context import pull_env_jinja_context
from .types import DBName, DBConfig, DBCLIConfig, JinjaContext, JinjaFilters, JinjaContextPuller
from typing import Dict, Tuple, Optional
import importlib
import pkgutil
import re
import logging


logger = logging.getLogger(__name__)


context_pullers: Optional[Dict[str, JinjaContextPuller]] = None


def get_context_pullers() -> Dict[str, JinjaContextPuller]:
    global context_pullers

    if context_pullers is not None:
        return context_pullers

    context_pullers = {
        'env': pull_env_jinja_context,
        'base64': pull_base64_jinja_context,
    }
    plugin_name_pattern = re.compile(r"^(.+_)?db_facts(_.+)?$")

    discovered_plugins = {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in pkgutil.iter_modules()
        if plugin_name_pattern.match(name) and name != 'db_facts'
    }
    for plugin_name, plugin_module in discovered_plugins.items():
        plugin_context_pullers = getattr(plugin_module, 'context_pullers', None)
        if plugin_context_pullers is None:
            logger.error(f"db-facts: Could not find context_pullers in {plugin_name} module")
        else:
            context_pullers.update(plugin_context_pullers)
            logger.info(f"db-facts: Added {plugin_context_pullers.keys()}")

    return context_pullers


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

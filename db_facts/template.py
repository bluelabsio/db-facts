import jinja2
from typing import Any, Tuple
from .db_facts_types import JinjaContext, JinjaFilters


def template(s: str, jinja_context_and_filters: Tuple[JinjaContext, JinjaFilters]) -> str:
    jinja_context, jinja_filters = jinja_context_and_filters
    environment = jinja2.Environment()
    environment.filters.update(jinja_filters)
    template = environment.from_string(s)
    return template.render(jinja_context)


def template_any(o: Any, jinja_context_and_filters: Tuple[JinjaContext, JinjaFilters]):
    if isinstance(o, str):
        return template(o, jinja_context_and_filters)
    else:
        return o

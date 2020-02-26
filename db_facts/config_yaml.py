from .db_facts_types import DBFacts
import yaml


def config_yaml(db_name: str, db_facts: DBFacts) -> str:
    config = {
        'dbs': {
            db_name: {
                'exports': db_facts
            },
        },
    }
    return yaml.dump(config)

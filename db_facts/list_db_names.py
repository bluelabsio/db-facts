from .config import load_config


def format_db_description(db_name, db_description):
    if db_description is not None:
        return f"{db_name} ({db_description})"
    else:
        return db_name


def list_db_names() -> None:
    dbcli_config = load_config()

    dbs = dbcli_config.get('dbs', {})
    db_descriptions = {
        db_name: db_config.get('description', None)
        for db_name, db_config
        in dbs.items()
    }

    output = [
        format_db_description(db_name, db_description)
        for db_name, db_description
        in db_descriptions.items()
    ]
    sorted_output = sorted(list(output))
    print("Available db_names:")
    print("* ", end='')
    print("\n* ".join(sorted_output))

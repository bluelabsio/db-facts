import pipes

formatted_key = {
    'password': 'DB_PASSWORD',
    'host': 'DB_HOST',
    'user': 'DB_USERNAME',
    'type': 'DB_TYPE',
    'protocol': 'DB_PROTOCOL',
    'port': 'DB_PORT',
    'database': 'DB_DATABASE',
}


def print_exports(exports):
    for k, v in sorted(exports.items()):
        env_var = formatted_key.get(k, k.upper())
        print("export " + env_var)
        print(env_var + "=" + pipes.quote(str(v)))

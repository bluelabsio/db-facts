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


def char_valid(char):
    return char.isalnum() or char == '_'


def only_valid_chars(string):
    return ''.join(filter(char_valid, string))


def format_key(key):
    if key in formatted_key:
        return formatted_key[key]

    return only_valid_chars(key).upper()


def print_exports(exports):
    for k, v in sorted(exports.items()):
        env_var = format_key(k)
        print("export " + env_var)
        print(env_var + "=" + pipes.quote(str(v)))

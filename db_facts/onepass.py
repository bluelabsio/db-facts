import json

import boto3

from .db_facts_types import AWSSecret, AWSSecretUsernamePassword
from .db_type import canonicalize_db_type, db_protocol
import re

"""
Takes a lastpass secret_id and translates it to the corresponding aws secret_id
"""
def translate_entry_name_to_onepass(entry_name: str) -> str:
    cms_secret_pattern = r'(CMS Vertica) (\([a-z]+\)): ([a-z]+)'
    cms_secret_pattern = re.compile(cms_secret_pattern)
    if cms_secret_pattern.match(entry_name):
        match = re.search(cms_secret_pattern, entry_name)
        stack = match.group(2).replace('(', '').replace(')', '')
        username = match.group(3)
        entry_name = f'{stack}_vertica_{username}_creds'
    else:
        raise NotImplementedError("Currently only CMS secret IDs can be translated to secretsmanager")
    return entry_name


def pull_onepass_secret(entry_name: str) -> AWSSecret:
    response = boto3.client("secretsmanager").get_secret_value(SecretId=entry_name)
    return json.loads(response["SecretString"])


def pull_onepass_username_password(
    entry_name: str,
) -> AWSSecretUsernamePassword:
    secret = pull_onepass_secret(entry_name)
    return {"user": secret["username"], "password": secret["password"]}


def db_info_from_onepass(entry_name: str):
    response = pull_onepass_secret(entry_name)

    result = {key.lower(): value for key, value in response.items()}

    result["host"] = result.pop("hostname")
    result["user"] = result.pop("username")

    # mypy has issues with `result.get('type')`
    # https://stackoverflow.com/questions/70955906/how-to-deal-with-incompatible-type-optionalstr-expected-str
    if "type" in result:
        result["type"] = canonicalize_db_type(result["type"])
        result["protocol"] = db_protocol(result["type"])
    else:
        result["type"] = ""
        result["protocol"] = ""

    return result

import json

import boto3

from .db_facts_types import AWSSecret, AWSSecretUsernamePassword
from .db_type import canonicalize_db_type, db_protocol


def pull_aws_secrets_manager_secret(sm_entry_name: str) -> AWSSecret:
    response = boto3.client("secretsmanager").get_secret_value(SecretId=sm_entry_name)
    return json.loads(response["SecretString"])


def pull_aws_secrets_manager_username_password(
    sm_entry_name: str,
) -> AWSSecretUsernamePassword:
    secret = pull_aws_secrets_manager_secret(sm_entry_name)
    return {"user": secret["username"], "password": secret["password"]}


def db_info_from_secrets_manager(sm_entry_name: str):
    response = pull_aws_secrets_manager_secret(sm_entry_name)

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

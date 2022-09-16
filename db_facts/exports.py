import logging
import pipes
from typing import Optional
from urllib.parse import quote, urlencode
from .db_facts_types import DBFacts

logger = logging.getLogger(__name__)

formatted_key = {
    "password": "DB_PASSWORD",
    "host": "DB_HOST",
    "user": "DB_USERNAME",
    "type": "DB_TYPE",
    "protocol": "DB_PROTOCOL",
    "port": "DB_PORT",
    "database": "DB_DATABASE",
}


def print_exports(exports: DBFacts):
    for k, v in sorted(exports.items()):
        env_var = formatted_key.get(k, k.upper())
        print("export " + env_var)
        print(env_var + "=" + pipes.quote(str(v)))


def print_airflow(exports: DBFacts):
    """Generically translate credentials into airflow credential string."""
    print(AirflowConnection(**exports).get_uri())


class AirflowConnection:
    """Copied from the apache-airflow airflow.operators.connection.Connection class

    Simplified to reproduce a minimal implementation of the get_uri() method.
    """

    conn_type: Optional[str]
    description: Optional[str]
    host: Optional[str]
    login: Optional[str]
    password: Optional[str]
    schema: Optional[str]
    port: Optional[int]
    extra: Optional[dict]

    def __init__(
        self,
        type: Optional[str] = None,
        description: Optional[str] = None,
        host: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        port: Optional[int] = None,
        **kwargs
    ):
        self.description = description
        self.conn_type = type
        self.host = host
        self.login = user or kwargs.pop('username')
        self.password = password
        self.schema = database
        self.port = port
        self.extra = kwargs

    def get_uri(self) -> str:
        """Return connection in URI format"""
        if isinstance(self.conn_type, str) and "_" in self.conn_type:
            logger.warning(
                f"Connection schemes (type: {str(self.conn_type)}) "
                f"shall not contain '_' according to RFC3986."
            )

        uri = f"{str(self.conn_type).lower().replace('_', '-')}://"

        authority_block = ""
        if self.login is not None:
            authority_block += quote(self.login, safe="")

        if self.password is not None:
            authority_block += ":" + quote(self.password, safe="")

        if authority_block > "":
            authority_block += "@"

            uri += authority_block

        host_block = ""
        if self.host:
            host_block += quote(self.host, safe="")

        if self.port:
            if host_block == "" and authority_block == "":
                host_block += f"@:{self.port}"
            else:
                host_block += f":{self.port}"

        if self.schema:
            host_block += f"/{quote(self.schema, safe='')}"

        uri += host_block

        if self.extra:
            uri += ("?" if self.schema else "/?") + urlencode(self.extra)

        return uri

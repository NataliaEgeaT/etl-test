import os
import pyodbc
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class MSSQLClient:
    """
    MSSQL Client using FreeTDS ODBC driver (compatible with ARM64).
    """

    def __init__(self, server=None, database=None, username=None, password=None):
        self.server = server or os.getenv("MSSQL_SERVER", "sqlserver")
        self.database = database or os.getenv("MSSQL_DATABASE", "etl_test")
        self.username = username or os.getenv("MSSQL_USER", "sa")
        self.password = password or os.getenv("MSSQL_PASSWORD", "YourStrong!Passw0rd")

        # FreeTDS driver string (ARM64-compatible)
        self.conn_str = (
            "DRIVER=FreeTDS;"
            "SERVER=sqlserver;"
            "PORT=1433;"
            "TDS_VERSION=8.0;"
            "DATABASE=etl_test;"
            "UID=sa;"
            "PWD=YourStrong!Passw0rd;"
            "ClientCharset=UTF-8;"
        )

    def query(self, sql):
        """
        Execute SQL query and return DataFrame.
        """
        logger.info(f"Executing MSSQL query: {sql}")

        try:
            conn = pyodbc.connect(self.conn_str)
        except Exception as conn_err:
            logger.error(f"Connection error: {conn_err}")
            raise

        try:
            df = pd.read_sql(sql, conn)
            return df
        except Exception as query_err:
            logger.error(f"Query error: {query_err}")
            raise
        finally:
            conn.close()



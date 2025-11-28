
import pyodbc
import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

class MSSQLClient:
    def __init__(self):
        self.conn_str = (
            f"DRIVER={os.environ['MSSQL_DRIVER']};"
            f"Servername={os.environ['MSSQL_SERVER']};"
            f"Database={os.environ['MSSQL_DATABASE']};"
            f"UID={os.environ['MSSQL_USER']};"
            f"PWD={os.environ['MSSQL_PASSWORD']};"
            f"TDS_Version={os.environ['MSSQL_TDS_VERSION']};"
            f"ClientCharset={os.environ['MSSQL_CHARSET']};"
        )

    def query(self, sql):
        logger.info(f"Executing MSSQL query: {sql}")
        conn = pyodbc.connect(self.conn_str)
        df = pd.read_sql(sql, conn)
        conn.close()
        return df

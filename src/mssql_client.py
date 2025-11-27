import os
import pyodbc
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class MSSQLClient:
    def __init__(self):
        self.conn_str = (
            "DRIVER=FreeTDS;"
            "Servername=sqlserver;"
            "Database=etl_test;"
            "UID=sa;"
            "PWD=YourStrong!Passw0rd;"
            "TDS_Version=8.0;"
            "ClientCharset=UTF-8;"
        )

    def query(self, sql):
        logger.info(f"Executing MSSQL query: {sql}")
        conn = pyodbc.connect(self.conn_str)
        df = pd.read_sql(sql, conn)
        conn.close()
        return df

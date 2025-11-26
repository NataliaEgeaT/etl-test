import pyodbc
import logging
import pandas as pd

logger = logging.getLogger(__name__)

class MSSQLClient:
    """Simple SQL Server client for SELECT queries."""

    def __init__(self, server, database, username=None, password=None, driver='{ODBC Driver 17 for SQL Server}'):
        self.conn_str = (
            f"DRIVER={driver};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            f"TrustServerCertificate=yes;"
        )

    def query(self, sql):
        logger.info(f"Executing MSSQL query: {sql}")
        conn = pyodbc.connect(self.conn_str)
        df = None
        try:
            df = pd.read_sql(sql, conn)
        finally:
            conn.close()

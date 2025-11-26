import pandas as pd
from src.mssql_client import MSSQLClient
import os

MSSQL_SERVER = os.getenv("MSSQL_SERVER", "localhost")
MSSQL_DATABASE = os.getenv("MSSQL_DATABASE", "etl_test")
MSSQL_USER = os.getenv("MSSQL_USER", "sa")
MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD", "YourStrong!Passw0rd")

client = MSSQLClient(
    server=MSSQL_SERVER,
    database=MSSQL_DATABASE,
    username=MSSQL_USER,
    password=MSSQL_PASSWORD
)

def load_users():
    return client.query("SELECT * FROM dbo.users")

def load_products():
    return client.query("SELECT * FROM dbo.products")

def load_legacy_orders():
    """Optional legacy support."""
    return client.query("SELECT * FROM dbo.orders_db")

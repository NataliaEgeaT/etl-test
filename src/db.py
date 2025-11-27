import duckdb
import os

DB_PATH = "duckdb_db/warehouse.db"

def get_connection():
    os.makedirs("duckdb_db", exist_ok=True)
    return duckdb.connect(DB_PATH, read_only=False)

def init_database():
    conn = get_connection()
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR,
            email VARCHAR,
            created_at DATE,
            country VARCHAR
        );
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            sku VARCHAR,
            name VARCHAR,
            category VARCHAR,
            price DOUBLE
        );
    """)

    # Only insert if empty
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        conn.execute("""
            INSERT INTO users VALUES
            ('u1', 'alice@example.com', '2024-01-01', 'US'),
            ('u2', 'bob@example.com', '2024-02-01', 'CO'),
            ('u3', 'carol@example.com', '2024-03-01', 'MX');
        """)

    if conn.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        conn.execute("""
            INSERT INTO products VALUES
            ('sku1', 'Laptop', 'electronics', 950.00),
            ('sku2', 'Mouse', 'electronics', 20.00),
            ('sku3', 'Keyboard', 'electronics', 49.00);
        """)

    conn.close()

def load_users():
    conn = get_connection()
    df = conn.execute("SELECT * FROM users").fetch_df()
    conn.close()
    return df

def load_products():
    conn = get_connection()
    df = conn.execute("SELECT * FROM products").fetch_df()
    conn.close()
    return df


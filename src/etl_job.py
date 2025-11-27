import argparse
import logging
from pathlib import Path
import pandas as pd

from src.api_client import APIClient
from src.transforms import normalize_orders, dedupe
from src.db import init_database, load_users, load_products
from src.utils import configure_logging

BASE_DIR = Path(__file__).resolve().parents[1]
SAMPLE_DATA = BASE_DIR / "sample_data"
OUTPUT = BASE_DIR / "output"

def save_raw(raw):
    raw_dir = OUTPUT / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    import json
    with open(raw_dir / "orders_raw.json", "w") as f:
        json.dump(raw, f, indent=2)

    logging.info(f"Saved raw JSON to {raw_dir}")

def write_curated(orders_df, items_df):
    curated_root = OUTPUT / "curated"
    curated_root.mkdir(parents=True, exist_ok=True)

    for date, df_part in orders_df.groupby("date"):
        partition_dir = curated_root / f"date={date}"
        partition_dir.mkdir(parents=True, exist_ok=True)

        df_part.to_parquet(partition_dir / "fact_order.parquet", index=False)
        subset_items = items_df[items_df["order_id"].isin(df_part["order_id"])]
        subset_items.to_parquet(partition_dir / "order_items.parquet", index=False)

        logging.info(f"Wrote curated partition: {partition_dir}")

def run_etl(since=None):
    configure_logging()
    logging.info(f"ETL started | since={since}")

    # Initialize DuckDB (creates tables + loads sample data if empty)
    init_database()

    # Extract
    api = APIClient(SAMPLE_DATA / "api_orders.json")
    raw_orders = api.get_orders()

    save_raw(raw_orders)

    # Dimension data
    users_df = load_users()
    products_df = load_products()

    # Transform
    orders_df, items_df = normalize_orders(raw_orders)

    if since:
        orders_df = orders_df[orders_df["created_at"] > since]
        items_df = items_df[items_df["order_id"].isin(orders_df["order_id"])]

    orders_df = dedupe(orders_df, "order_id")
    items_df = dedupe(items_df, "order_id")

    if orders_df.empty:
        logging.warning("No orders to load after filtering")
        return

    # Load
    write_curated(orders_df, items_df)

    logging.info("ETL finished successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", required=False)
    args = parser.parse_args()
    run_etl(since=args.since)


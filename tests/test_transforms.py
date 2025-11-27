import pandas as pd
from src.transforms import normalize_orders, dedupe
import json
from pathlib import Path
from src.api_client import APIClient


def test_normalize_orders_valid():
    raw = [
        {
            "order_id": "o_1",
            "user_id": "u_1",
            "amount": 50,
            "currency": "USD",
            "created_at": "2025-01-01T10:00:00Z",
            "items": [{"sku": "p_1", "qty": 2, "price": 25}]
        }
    ]

    orders_df, items_df = normalize_orders(raw)

    assert len(orders_df) == 1
    assert len(items_df) == 1
    assert orders_df.iloc[0]["order_id"] == "o_1"
    assert items_df.iloc[0]["sku"] == "p_1"


def test_normalize_orders_discard_malformed():
    raw = [
        {"order_id": None, "created_at": "2025-01-01T10:00:00Z"},  # malformed
        {"order_id": "o_2", "created_at": None},                    # malformed
        {"order_id": "o_3", "created_at": "2025-01-02T10:00:00Z"}   # valid
    ]

    orders_df, items_df = normalize_orders(raw)

    assert len(orders_df) == 1
    assert orders_df.iloc[0]["order_id"] == "o_3"


def test_dedupe_keep_latest():
    df = pd.DataFrame({
        "order_id": ["o_1", "o_1"],
        "amount": [10, 20]
    })

    result = dedupe(df, "order_id")

    assert len(result) == 1
    assert result.iloc[0]["amount"] == 20


def test_items_empty_list_ok():
    raw = [
        {
            "order_id": "o_10",
            "created_at": "2025-01-01T10:00:00Z",
            "user_id": "u_5",
            "items": []
        }
    ]

    orders_df, items_df = normalize_orders(raw)

    assert len(orders_df) == 1
    assert items_df.empty


def test_missing_price_is_allowed():
    raw = [
        {
            "order_id": "o_20",
            "created_at": "2025-01-01T10:00:00Z",
            "user_id": "u_6",
            "items": [{"sku": "p_10", "qty": 1, "price": None}]
        }
    ]

    orders_df, items_df = normalize_orders(raw)

    assert items_df.iloc[0]["price"] is None

def test_incremental_filter():
    raw = [
        {"order_id": "o_1", "created_at": "2025-01-01T10:00:00Z"},
        {"order_id": "o_2", "created_at": "2025-01-10T10:00:00Z"}
    ]

    orders_df, _ = normalize_orders(raw)
    filtered = orders_df[orders_df["created_at"] > "2025-01-05T00:00:00Z"]

    assert len(filtered) == 1
    assert filtered.iloc[0]["order_id"] == "o_2"

def test_api_client_reads_file(tmp_path):
    sample = tmp_path / "api.json"
    sample.write_text(json.dumps([{"order_id": "o_1"}]))

    client = APIClient(sample)
    data = client.get_orders()

    assert data[0]["order_id"] == "o_1"

def test_incremental_filter():
    raw = [
        {"order_id": "A1", "created_at": "2025-01-01T00:00:00Z", "items": []},
        {"order_id": "A2", "created_at": "2026-01-01T00:00:00Z", "items": []}
    ]

    orders, _ = normalize_orders(raw)

    filtered = orders[orders["created_at"] > "2025-06-01T00:00:00Z"]

    assert set(filtered["order_id"]) == {"A2"}
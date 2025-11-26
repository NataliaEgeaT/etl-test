import logging
import pandas as pd

logger = logging.getLogger(__name__)

def normalize_orders(raw_orders):
    """Normalize nested API structure into fact_order and order_items."""

    orders = []
    items = []
    discarded = 0

    for o in raw_orders:
        try:
            order_id = o.get("order_id")
            created_at = o.get("created_at")

            # Skip malformed
            if not order_id or not created_at:
                discarded += 1
                continue

            date = created_at[:10]

            orders.append({
                "order_id": order_id,
                "user_id": o.get("user_id"),
                "amount": o.get("amount", 0.0),
                "currency": o.get("currency", "USD"),
                "created_at": created_at,
                "date": date
            })

            # Items
            for it in o.get("items", []):
                items.append({
                    "order_id": order_id,
                    "sku": it.get("sku"),
                    "qty": it.get("qty", 0),
                    "price": it.get("price")
                })

        except Exception:
            discarded += 1

    logger.info(
        f"Normalization summary: {len(orders)} orders, "
        f"{len(items)} items, {discarded} discarded"
    )

    return pd.DataFrame(orders), pd.DataFrame(items)


def dedupe(df, key):
    """Remove duplicates by key, keep last one."""
    if df.empty:
        return df
    return df.sort_values(key).drop_duplicates(subset=[key], keep="last")

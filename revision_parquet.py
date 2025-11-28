import pandas as pd

df_orders = pd.read_parquet("output/curated/date=2025-08-20/fact_order.parquet")
df_items = pd.read_parquet("output/curated/date=2025-08-20/order_items.parquet")

print(df_orders)
print(df_items)

1. Architecture Overview
The pipeline follows a clean Extract → Transform → Load (ETL) architecture, fully executable both locally and inside Docker, ensuring reproducibility.

API Mock (JSON)
        ↓
     Raw Layer
        ↓
Transformations (Pandas + DuckDB)
        ↓
 Partitioned Curated Layer (Parquet)
            
Users CSV + Products CSV ┘

The ETL can be executed through:
python -m src.etl_job
python -m src.etl_job --since <timestamp>

Outputs stored in:
output/raw/
output/curated/

2. Extraction
Sources:
- api_orders.json — simulated REST API response.
- users.csv / products.csv — dimension tables.

API robustness:
- Retry mechanism
- Delay between retries
- Handles malformed JSON
- Complete logging

3. Transformations
Normalization:
- orders_df → one row per order
- items_df → one row per item

Derived fields:
- date extracted from created_at for partitioning

Record cleaning:
- Discard orders missing order_id or created_at
- Logs discarded count

Deduplication:
- dedupe(df, key="order_id")
- Latest record wins (idempotency)

4. Incremental Processing
Executed using:
python -m src.etl_job --since "2025-01-15T00:00:00Z"

Incremental logic:
- Filters orders by timestamp
- Items kept only for surviving order_id

5. Loading Strategy
Raw layer:
output/raw/orders_raw.json

Curated layer (Parquet partitioned):
output/curated/date=YYYY-MM-DD/fact_order.parquet
output/curated/date=YYYY-MM-DD/order_items.parquet

Partitions are overwritten each run (idempotent).

6. Data Model (Redshift-Compatible)
dim_user: user_id, email, created_at, country
dim_product: sku, name, category, price
fact_order: order_id, user_id, sku, amount, qty, price, created_at, date

7. Monitoring & Logging
Logs:
- Run start/end
- Extracted records
- Discarded records
- Partitions written
- API retry attempts

Production alerts would include:
- Retry exhaustion
- No new incremental data
- High discard percentage

8. Technology Choices
Pandas + PyArrow + DuckDB:
Reasons:

- Fast local execution
- Extremely lightweight
- Ideal for medium-volume analytical tasks
- Simpler than PySpark, but with high performance
- Supports Parquet natively

Docker

Benefits:

- Fully reproducible environment
- Evaluators can run the project without installing Python or dependencies
- Matches real-world CI/CD and deployment patterns

Execution example:
docker-compose run --rm app python -m src.etl_job

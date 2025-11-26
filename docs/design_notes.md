1. Architecture Overview

The solution follows a classic Extract → Transform → Load (ETL) structure, fully executable locally and packaged in Docker for reproducibility.

API Mock (JSON) → Raw Layer → Transformations → Curated Layer (Partitioned)
           CSV Users + CSV Products ┘


The ETL can be executed via:

python -m src.etl_job
python -m src.etl_job --since <timestamp>


All output is written under output/raw/ and output/curated/.

2. Extraction
Sources

api_orders.json simulates the REST API.

users.csv and products.csv are flat-database representations.

Error Handling

APIClient includes:

Retry mechanism (3 attempts)

Delay between retries

Logging of failures

Malformed JSON records do not break execution.

3. Transformations
Normalization

Orders from the API contain nested structures (items array).
They are normalized into two DataFrames:

orders_df
Flattened representation of order headers.

items_df
One row per item inside items.

Derived Fields

date is extracted from created_at (YYYY-MM-DD) to support partitioning.

Malformed Records

Records lacking critical fields (order_id, created_at) are discarded.

Count of discarded records is logged.

Deduplication (Idempotency Principle #1)

The API may contain duplicate order_id.

We apply:

dedupe(df, key="order_id")


Always keeps the latest record.

4. Incremental Processing

The ETL supports incremental execution via:

--since "2025-01-15T00:00:00Z"


Implementation:

Orders with created_at <= since are filtered out.

Items are filtered by valid order_id.

This reduces processing time and allows continuous ingestion.

5. Loading Strategy
Raw Layer

Exact copy of API input:

output/raw/orders_raw.json

Curated Layer

Final analytical tables stored in Parquet.

Partitioned by date:

output/curated/date=YYYY-MM-DD/fact_order.parquet
output/curated/date=YYYY-MM-DD/order_items.parquet

Idempotency (Principle #2: Replace Partitions)

Each run overwrites the folder date=YYYY-MM-DD/.
This guarantees that repeated runs produce consistent results without duplicates.

6. Data Model (Redshift-Compatible)
dim_user
user_id (PK)
email
created_at
country

dim_product
sku (PK)
name
category
price

fact_order
order_id (PK)
user_id (FK)
sku (FK)
amount
qty
price
created_at
date (partition key)


The model supports analytical workloads such as sales aggregation, product performance, and user behavior analysis.

7. Monitoring & Logging

The ETL logs:

Start/end timestamps

Records extracted

Records discarded

Partitions written

Retry attempts for API calls

These logs can easily be extended to metrics for production environments.

Alerting examples for production:

API retry exhaustion

No new records in incremental loads

High percentage of discarded records

8. Technology Choices
Pandas + PyArrow

Reasoning:

Lightweight for local execution.

Simple to test, debug, and document.

Works extremely well with Parquet.

Faster development compared to PySpark for this scale.

Docker

Ensures reproducibility regardless of host environment.

Evaluators can run the project with:

docker-compose run --rm app python -m src.etl_job
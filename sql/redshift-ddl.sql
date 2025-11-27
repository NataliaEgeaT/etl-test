-- ==========================================
-- Data Warehouse Schema – Redshift Compatible
-- ==========================================

-- DIMENSION: dim_user

CREATE TABLE dim_user (
    user_id        VARCHAR(64) PRIMARY KEY,
    email          VARCHAR(255),
    created_at     DATE,
    country        VARCHAR(8)
);

-- DIMENSION: dim_product

CREATE TABLE dim_product (
    sku            VARCHAR(64) PRIMARY KEY,
    name           VARCHAR(255),
    category       VARCHAR(150),
    price          DECIMAL(12,2)
);

-- FACT TABLE: fact_order

CREATE TABLE fact_order (
    order_id       VARCHAR(64) PRIMARY KEY,
    user_id        VARCHAR(64),
    amount         DECIMAL(12,2),      
    currency       VARCHAR(10),
    created_at     TIMESTAMP,
    date           DATE
);

-- FACT TABLE: order_items

CREATE TABLE fact_order_item (
    order_id       VARCHAR(64),
    sku            VARCHAR(64),
    qty            INTEGER,
    price          DECIMAL(12,2),

    PRIMARY KEY (order_id, sku)
);

-- ==========================
-- Helpful Queries for Review
-- ==========================

-- Deduplicate orders by order_id (latest wins)
-- SELECT *
-- FROM fact_order
-- QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY created_at DESC) = 1;

-- Orders per day
-- SELECT date, COUNT(*)
-- FROM fact_order
-- GROUP BY date
-- ORDER BY date;

-- Revenue by product
-- SELECT i.sku, SUM(i.qty * i.price) AS revenue
-- FROM fact_order_item i
-- GROUP BY i.sku
-- ORDER BY revenue DESC;


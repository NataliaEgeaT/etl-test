-- ==========================================
-- Data Warehouse Schema – Redshift Compatible
-- ==========================================

-- =====================
-- DIMENSION: dim_user
-- =====================
CREATE TABLE dim_user (
    user_id        VARCHAR(64) PRIMARY KEY,
    email          VARCHAR(255),
    created_at     DATE,
    country        VARCHAR(8)
);


-- ========================
-- DIMENSION: dim_product
-- ========================
CREATE TABLE dim_product (
    sku            VARCHAR(64) PRIMARY KEY,
    name           VARCHAR(255),
    category       VARCHAR(150),
    price          DECIMAL(12,2)
);


-- =====================
-- FACT TABLE: fact_order
-- =====================
CREATE TABLE fact_order (
    order_id       VARCHAR(64) PRIMARY KEY,
    user_id        VARCHAR(64),
    sku            VARCHAR(64),
    amount         DECIMAL(12,2),
    qty            INTEGER,
    price          DECIMAL(12,2),
    created_at     TIMESTAMP,
    date           DATE,

    -- Foreign keys (not enforced by Redshift but documented)
    -- REFERENCES dim tables
    -- user_id      REFERENCES dim_user(user_id),
    -- sku          REFERENCES dim_product(sku)
);

-- ==========================
-- Helpful Queries for Review
-- ==========================

-- Deduplicate orders by order_id (latest wins)
-- SELECT * FROM fact_order QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY created_at DESC) = 1;

-- Count orders by date
-- SELECT date, COUNT(*) FROM fact_order GROUP BY date ORDER BY date;

-- Total revenue per product
-- SELECT sku, SUM(amount) AS total_sales
-- FROM fact_order
-- GROUP BY sku
-- ORDER BY total_sales DESC;

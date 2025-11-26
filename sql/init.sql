-- Create database 
IF DB_ID('etl_test') IS NULL
BEGIN
    CREATE DATABASE etl_test;
END;
GO

USE etl_test;
GO


IF OBJECT_ID('dbo.users', 'U') IS NOT NULL DROP TABLE dbo.users;
IF OBJECT_ID('dbo.products', 'U') IS NOT NULL DROP TABLE dbo.products;
IF OBJECT_ID('dbo.orders_db', 'U') IS NOT NULL DROP TABLE dbo.orders_db;
GO

-- =========================
-- USERS TABLE (DIMENSION)
-- =========================

CREATE TABLE dbo.users (
    user_id    VARCHAR(64) PRIMARY KEY,
    email      VARCHAR(255),
    created_at DATE,
    country    VARCHAR(8)
);

-- =========================
-- PRODUCTS TABLE (DIMENSION)
-- =========================

CREATE TABLE dbo.products (
    sku       VARCHAR(64) PRIMARY KEY,
    name      VARCHAR(255),
    category  VARCHAR(150),
    price     DECIMAL(12,2)
);


-- =========================
-- LEGACY ORDERS TABLE (FACT)
-- =========================

CREATE TABLE dbo.orders_db (
    order_id      VARCHAR(64) PRIMARY KEY,
    user_id       VARCHAR(64),
    total_amount  DECIMAL(12,2),
    created_at    DATETIME2,
    metadata      NVARCHAR(MAX)
);



INSERT INTO dbo.users (user_id, email, created_at, country) VALUES
('u_1', 'user1@example.com', '2024-01-01', 'US'),
('u_2', 'user2@example.com', '2024-02-10', 'ES'),
('u_3', 'user3@example.com', '2024-03-15', 'CO');

INSERT INTO dbo.products (sku, name, category, price) VALUES
('p_1', 'Product 1', 'Category A', 60.00),
('p_2', 'Product 2', 'Category B', 35.50),
('p_3', 'Product 3', 'Category C', 120.00);

INSERT INTO dbo.orders_db (order_id, user_id, total_amount, created_at, metadata) VALUES
('o_legacy_1', 'u_1', 100.00, '2024-04-01T10:00:00', N'{"source":"legacy"}'),
('o_legacy_2', 'u_2', 250.00, '2024-05-02T15:30:00', N'{"source":"legacy"}');

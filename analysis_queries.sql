-- ============================================
-- E-Commerce Analytics Queries
-- SQLite version
-- ============================================

-- Query 1: Monthly Revenue Trend
-- Business Question: How is revenue trending month over month?
SELECT 
    strftime('%Y-%m', order_purchase_timestamp) AS month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS monthly_revenue
FROM orders o
JOIN payments p ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY month
ORDER BY month;

-- Query 2: RFM Base Calculation
-- Business Question: Which customers are most valuable?
WITH rfm_base AS (
    SELECT
        o.customer_id,
        MAX(o.order_purchase_timestamp) AS last_order_date,
        COUNT(DISTINCT o.order_id) AS frequency,
        SUM(p.payment_value) AS monetary
    FROM orders o
    JOIN payments p ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY o.customer_id
)
SELECT 
    customer_id,
    last_order_date,
    frequency,
    ROUND(monetary, 2) AS monetary
FROM rfm_base
ORDER BY monetary DESC
LIMIT 100;

-- Query 3: Product Category Margin Analysis
-- Business Question: Which categories have highest/lowest gross margin?
SELECT
    pr.product_category_name_english AS category,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS gross_revenue,
    ROUND(SUM(oi.price * pr.cost_price / pr.sale_price), 2) AS total_cost,
    ROUND(SUM(oi.price - (oi.price * pr.cost_price / pr.sale_price)), 2) AS gross_profit,
    ROUND(SUM(oi.price - (oi.price * pr.cost_price / pr.sale_price)) 
        * 100.0 / SUM(oi.price), 1) AS margin_pct
FROM order_items oi
JOIN products pr ON oi.product_id = pr.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY category
ORDER BY margin_pct DESC;

-- Query 4: Revenue by State
-- Business Question: Which regions are growing vs declining?
SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS total_revenue,
    ROUND(AVG(p.payment_value), 2) AS avg_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN payments p ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY total_revenue DESC;

-- Query 5: Payment Method Analysis
-- Business Question: Which payment methods correlate with higher order values?
SELECT
    payment_type,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(payment_value), 2) AS avg_order_value,
    ROUND(SUM(payment_value), 2) AS total_revenue
FROM payments
GROUP BY payment_type
ORDER BY avg_order_value DESC;

-- Query 6: Order Status Distribution
-- Business Question: What percentage of orders are delivered vs cancelled?
SELECT
    order_status,
    COUNT(*) AS total_orders,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS percentage
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;

-- Query 7: Top 10 Revenue Categories
-- Business Question: Which categories drive 80% of revenue?
SELECT
    pr.product_category_name_english AS category,
    ROUND(SUM(oi.price), 2) AS total_revenue,
    ROUND(SUM(oi.price) * 100.0 / 
        (SELECT SUM(price) FROM order_items), 2) AS revenue_pct
FROM order_items oi
JOIN products pr ON oi.product_id = pr.product_id
GROUP BY category
ORDER BY total_revenue DESC
LIMIT 10;

-- Query 8: Average Delivery Days by State
-- Business Question: Which regions have worst delivery performance?
SELECT
    c.customer_state,
    ROUND(AVG(
        JULIANDAY(o.order_delivered_customer_date) - 
        JULIANDAY(o.order_purchase_timestamp)
    ), 1) AS avg_delivery_days,
    COUNT(*) AS total_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
AND o.order_delivered_customer_date IS NOT NULL
GROUP BY c.customer_state
ORDER BY avg_delivery_days DESC;

-- Query 9: Monthly Cohort Retention
-- Business Question: Where does retention collapse?
WITH first_purchase AS (
    SELECT 
        customer_id,
        strftime('%Y-%m', MIN(order_purchase_timestamp)) AS cohort_month
    FROM orders
    WHERE order_status = 'delivered'
    GROUP BY customer_id
),
monthly_activity AS (
    SELECT 
        o.customer_id,
        strftime('%Y-%m', o.order_purchase_timestamp) AS activity_month,
        fp.cohort_month
    FROM orders o
    JOIN first_purchase fp ON o.customer_id = fp.customer_id
),
cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT customer_id) AS cohort_customers
    FROM first_purchase
    GROUP BY cohort_month
)
SELECT 
    ma.cohort_month,
    ma.activity_month,
    COUNT(DISTINCT ma.customer_id) AS active_customers,
    cs.cohort_customers,
    ROUND(COUNT(DISTINCT ma.customer_id) * 100.0 / cs.cohort_customers, 1) AS retention_pct
FROM monthly_activity ma
JOIN cohort_size cs ON ma.cohort_month = cs.cohort_month
GROUP BY ma.cohort_month, ma.activity_month
ORDER BY ma.cohort_month, ma.activity_month
LIMIT 200;

-- Query 10: Seller Performance
-- Business Question: Which sellers have worst on-time rate?
SELECT
    oi.seller_id,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(AVG(
        JULIANDAY(o.order_delivered_customer_date) - 
        JULIANDAY(o.order_purchase_timestamp)
    ), 1) AS avg_delivery_days,
    SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date 
        THEN 1 ELSE 0 END) AS late_orders,
    ROUND(SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date 
        THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS late_rate_pct
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
AND o.order_delivered_customer_date IS NOT NULL
GROUP BY oi.seller_id
HAVING total_orders >= 10
ORDER BY late_rate_pct DESC
LIMIT 20;
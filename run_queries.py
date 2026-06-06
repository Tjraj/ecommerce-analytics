import sqlite3
import pandas as pd
import os

# Connect
conn = sqlite3.connect('ecommerce.db')
print("Connected to database.")

# Create exports folder
os.makedirs('exports', exist_ok=True)

# Query 1 - Monthly Revenue
q1 = """
SELECT 
    strftime('%Y-%m', order_purchase_timestamp) AS month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS monthly_revenue
FROM orders o
JOIN payments p ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY month
ORDER BY month;
"""
df1 = pd.read_sql_query(q1, conn)
df1.to_csv('exports/monthly_revenue.csv', index=False)
print(f"Query 1 done. {len(df1)} rows.")

# Query 2 - RFM
q2 = """
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
SELECT customer_id, last_order_date, frequency, ROUND(monetary,2) AS monetary
FROM rfm_base
ORDER BY monetary DESC;
"""
df2 = pd.read_sql_query(q2, conn)
df2.to_csv('exports/rfm_scores.csv', index=False)
print(f"Query 2 done. {len(df2)} rows.")

# Query 3 - Margin Analysis
q3 = """
SELECT
    pr.product_category_name_english AS category,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS gross_revenue,
    ROUND(SUM(oi.price - (oi.price * pr.cost_price / pr.sale_price)), 2) AS gross_profit,
    ROUND(SUM(oi.price - (oi.price * pr.cost_price / pr.sale_price)) 
        * 100.0 / SUM(oi.price), 1) AS margin_pct
FROM order_items oi
JOIN products pr ON oi.product_id = pr.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY category
ORDER BY margin_pct DESC;
"""
df3 = pd.read_sql_query(q3, conn)
df3.to_csv('exports/margin_analysis.csv', index=False)
print(f"Query 3 done. {len(df3)} rows.")

# Query 4 - Revenue by State
q4 = """
SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS total_revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN payments p ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY total_revenue DESC;
"""
df4 = pd.read_sql_query(q4, conn)
df4.to_csv('exports/revenue_by_state.csv', index=False)
print(f"Query 4 done. {len(df4)} rows.")

# Query 5 - Cohort Retention
q5 = """
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
ORDER BY ma.cohort_month, ma.activity_month;
"""
df5 = pd.read_sql_query(q5, conn)
df5.to_csv('exports/cohort_retention.csv', index=False)
print(f"Query 5 done. {len(df5)} rows.")

conn.close()
print("\nAll queries complete. CSVs saved to exports folder.")
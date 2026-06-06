import sqlite3
import pandas as pd
import os

# Connect to SQLite database (creates file if not exists)
conn = sqlite3.connect('../sql/ecommerce.db')
print("Database connected.")

# Load CSVs
customers = pd.read_csv('../data/raw/olist_customers_dataset.csv')
orders = pd.read_csv('../data/raw/olist_orders_dataset.csv')
order_items = pd.read_csv('../data/raw/olist_order_items_dataset.csv')
payments = pd.read_csv('../data/raw/olist_order_payments_dataset.csv')
products = pd.read_csv('../data/processed/products_extended.csv')

# Load into SQLite
customers.to_sql('customers', conn, if_exists='replace', index=False)
print("customers loaded.")

orders.to_sql('orders', conn, if_exists='replace', index=False)
print("orders loaded.")

order_items.to_sql('order_items', conn, if_exists='replace', index=False)
print("order_items loaded.")

payments.to_sql('payments', conn, if_exists='replace', index=False)
print("payments loaded.")

products.to_sql('products', conn, if_exists='replace', index=False)
print("products loaded.")

conn.close()
print("All 5 tables loaded successfully.")
import pandas as pd
import numpy as np
import os

# Load files
products = pd.read_csv('../data/raw/olist_products_dataset.csv')
translation = pd.read_csv('../data/raw/product_category_name_translation.csv')

# Merge English names
products = products.merge(translation, on='product_category_name', how='left')

# Seed
np.random.seed(42)

# Margin by category
category_margins = {
    'health_beauty': 0.45,
    'computers_accessories': 0.25,
    'auto': 0.30,
    'bed_bath_table': 0.40,
    'furniture_decor': 0.35,
    'sports_leisure': 0.38,
    'perfumery': 0.50,
    'housewares': 0.42,
    'telephony': 0.20,
    'watches_gifts': 0.45,
}

DEFAULT_MARGIN = 0.35

def get_margin(category):
    return category_margins.get(str(category).lower(), DEFAULT_MARGIN)

products['margin'] = products['product_category_name_english'].apply(get_margin)
products['sale_price'] = np.random.uniform(20, 500, size=len(products)).round(2)
products['cost_price'] = (products['sale_price'] * (1 - products['margin'])).round(2)

# Save
os.makedirs('../data/processed', exist_ok=True)
products.to_csv('../data/processed/products_extended.csv', index=False)

print(f"Done. {len(products)} products saved.")
print(products[['product_id','product_category_name_english','cost_price','sale_price']].head())
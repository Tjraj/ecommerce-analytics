# E-Commerce Revenue Optimisation & Customer Lifecycle Analytics

![Tools](https://img.shields.io/badge/Excel-217346?style=flat&logo=microsoft-excel&logoColor=white)
![Tools](https://img.shields.io/badge/SQL-SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Tools](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Tools](https://img.shields.io/badge/PowerBI-F2C811?style=flat&logo=powerbi&logoColor=black)

## Business Problem
An online retailer had 5 years of transaction data across 100,000+ orders but no clear answers to: Which customers are worth acquiring? Where is margin being lost? Which regions are growing? This project builds complete analytics infrastructure to answer all of these.

## Dataset
- **Source:** [Olist Brazilian E-Commerce Dataset — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **Size:** 99,441 orders | 96,477 customers | 112,650 order items
- **Period:** 2016–2018
- **Tables:** Customers, Orders, Order Items, Payments, Products (extended with synthetic cost_price)

## Tools & Why
- **Excel** — Initial data profiling, pivot tables, what-if pricing analysis, RAG KPI dashboard
- **SQL (SQLite)** — Cohort retention CTEs, RFM scoring, margin analysis, window functions
- **Python** — EDA visualisations, RFM segmentation, IsolationForest anomaly detection, CLV calculation
- **Power BI** — 3-page executive dashboard with DAX measures, star schema, cross-filtering

## Key Findings
- Top 20% of customers drive 53% of total revenue — classic Pareto distribution
- Cohort retention collapses after month 1 — most customers never make a second purchase
- Credit card orders have highest average order value at R$163 vs vouchers at R$66
- São Paulo dominates geographic revenue — top state by significant margin
- 3,380 anomalous orders detected (3%) — potential pricing errors or fraud worth R$280,000
- Average delivery time is 12.1 days with significant right-skew — some orders take 100+ days
- Health & Beauty and Watches & Gifts are top revenue categories

## Dashboard Screenshots
### Page 1 — Executive Overview
![Executive Overview](POWER%20BI/page1_executive.png.png)

### Page 2 — Customer Analytics
![Customer Analytics](POWER%20BI/page2_customer.png.png)

### Page 3 — Product Analytics
![Product Analytics](POWER%20BI/page3_product.png.png)

## Business Recommendations
1. **Re-engagement campaign** for at-risk customers — if 10% reactivated at avg CLV R$160, revenue uplift ~R$308,000
2. **Investigate 3,380 anomalous orders** — pattern suggests pricing errors recoverable through corrected invoicing
3. **Double down on Health & Beauty** — highest revenue category with strong margins, prioritise in marketing budget

## Project Structure

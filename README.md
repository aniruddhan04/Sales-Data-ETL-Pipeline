# 🧾 Sales Data ETL Pipeline and Dashboard

This project is a simple ETL (Extract, Transform, Load) pipeline built in Python that processes sales CSV files, loads the cleaned and aggregated data into a PostgreSQL database, and generates revenue trend visualizations for daily and monthly sales.

## 📦 Features

- Extracts raw sales data from CSV files
- Cleans and transforms data (e.g., calculates revenue)
- Loads raw and summary tables into a PostgreSQL database
- Visualizes daily and monthly revenue trends using Matplotlib

## 🧰 Technologies Used

- **Python 3**
- **Pandas** for data manipulation
- **SQLAlchemy** for database interaction
- **PostgreSQL** as the backend database
- **Matplotlib** for data visualization

## 📂 Project Structure

```
sales-data-etl-dashboard/
├── jan_sales.csv
├── feb_sales.csv
├── mar_sales.csv
├── sales_data_etl_dashboard.py    # Main ETL and visualization script
└── README.md                      # Project documentation
```

## 📊 Database Tables

| Table Name       | Description                            |
|------------------|----------------------------------------|
| `raw_sales`      | Raw sales data with revenue calculated |
| `daily_sales`    | Aggregated daily revenue               |
| `monthly_sales`  | Aggregated monthly revenue             |

## 🛠️ How to Run

1. **Install Dependencies**  
   Make sure you have PostgreSQL installed and running.

   ```bash
   pip install pandas sqlalchemy matplotlib psycopg2
   ```

2. **Set Up Your Database**

   Create a PostgreSQL database (e.g. `salesDB`) and update your connection string inside `sales_data_etl_dashboard.py`:

   ```python
   DATABASE_URL = "postgresql://postgres:admin@localhost:5433/salesDB"
   ```

3. **Add Your Data**  
   Place your sales CSV files in the `data/` folder.

4. **Run the Script**

   ```bash
   python sales_data_etl_dashboard.py
   ```

   It will:
   - Load and clean data
   - Write to PostgreSQL
   - Display daily and monthly revenue graphs

## 🧪 Example CSV Format

Each CSV file should have the following columns:

```csv
date,product_id,quantity,price
2025-01-03,P001,5,19.99
2025-01-04,P002,2,49.99
```

## 📈 Output

- **Daily Revenue Trend:** line plot showing revenue over time
- **Monthly Revenue Trend:** bar chart of total revenue per month

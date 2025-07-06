"""
sales_data_etl_dashboard.py
Sales Data ETL Pipeline and Dashboard
"""

import os
import glob
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, Float, String, Date, MetaData
import matplotlib.pyplot as plt

# Configuration
DATA_DIR = "."
CSV_PATTERN = "*.csv"

# Example for PostgreSQL:
# PostgreSQL connection for local instance
DATABASE_URL = "postgresql://postgres:admin@localhost:5433/salesDB"

# Table names
RAW_TABLE = "raw_sales"
SUMMARY_TABLE = "sales_summary"

def extract_csv_files(data_dir, pattern):
    """Read all CSV files matching pattern into a single DataFrame."""
    file_paths = glob.glob(os.path.join(data_dir, pattern))
    df_list = []
    for file in file_paths:
        print(f"Extracting {file}")
        df = pd.read_csv(file)
        df_list.append(df)
    if df_list:
        return pd.concat(df_list, ignore_index=True)
    else:
        return pd.DataFrame()


def transform_data(df):
    """Clean data and compute revenue."""
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()
    # Parse date column
    df['date'] = pd.to_datetime(df['date'])
    # Handle missing numeric values
    df['quantity'] = df['quantity'].fillna(0).astype(int)
    df['price'] = df['price'].fillna(0.0).astype(float)
    # Calculate revenue
    df['revenue'] = df['quantity'] * df['price']
    return df


def load_data(df, engine):
    """Create tables and load raw and summary data into the database."""
    metadata = MetaData()
    raw_sales = Table(
        RAW_TABLE, metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('date', Date),
        Column('product_id', String),
        Column('quantity', Integer),
        Column('price', Float),
        Column('revenue', Float),
        extend_existing=True
    )
    sales_summary = Table(
        SUMMARY_TABLE, metadata,
        Column('date', Date, primary_key=True),
        Column('daily_sales', Float),
        Column('monthly_sales', Float),
        extend_existing=True
    )
    metadata.create_all(engine)

    # Load raw data
    df.to_sql(RAW_TABLE, engine, if_exists='append', index=False)

    # Prepare summary data
    daily = df.groupby(df['date'].dt.date)['revenue'].sum().reset_index()
    daily.columns = ['date', 'daily_sales']
    monthly = df.groupby(df['date'].dt.to_period('M'))['revenue'].sum().reset_index()
    monthly['date'] = monthly['date'].dt.to_timestamp()
    monthly.columns = ['date', 'monthly_sales']

    # Ensure both 'date' columns are datetime for accurate merge
    daily['date'] = pd.to_datetime(daily['date'])
    monthly['date'] = pd.to_datetime(monthly['date'])

    daily.to_sql("daily_sales", engine, if_exists='replace', index=False)
    monthly.to_sql("monthly_sales", engine, if_exists='replace', index=False)

def visualize(engine):
    """Plot daily and monthly sales trends."""
    daily = pd.read_sql_table("daily_sales", engine)
    monthly = pd.read_sql_table("monthly_sales", engine)

    daily['date'] = pd.to_datetime(daily['date'])
    monthly['date'] = pd.to_datetime(monthly['date'])

    daily.sort_values('date', inplace=True)
    monthly.sort_values('date', inplace=True)

    # Plot daily sales
    plt.figure(figsize=(10, 4))
    plt.plot(daily['date'], daily['daily_sales'], marker='o', label='Daily Sales')
    plt.title('Daily Revenue Trend')
    plt.xlabel('Date')
    plt.ylabel('Daily Revenue ($)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot monthly sales
    plt.figure(figsize=(8, 4))
    plt.bar(monthly['date'], monthly['monthly_sales'], color='orange')
    plt.title('Monthly Revenue Trend')
    plt.xlabel('Month')
    plt.ylabel('Monthly Revenue ($)')
    plt.tight_layout()
    plt.show()


def main():
    # Initialize database connection
    engine = create_engine(DATABASE_URL)

    # Extract
    raw_df = extract_csv_files(DATA_DIR, CSV_PATTERN)
    if raw_df.empty:
        print("No data files found. Please add CSV files to the data directory.")
        return

    # Transform
    df = transform_data(raw_df)

    # Load
    load_data(df, engine)

    # Visualize
    visualize(engine)


if __name__ == "__main__":
    main()

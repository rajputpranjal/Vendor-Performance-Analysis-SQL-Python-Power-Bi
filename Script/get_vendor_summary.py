import pandas as pd
import sqlite3
import logging
from sqlalchemy import create_engine
from ingestion_db import ingest_db
import ingestion_db
import importlib

logging.basicConfig(
    filename = "logs/ingestion_db.log",
    level = logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    filemode = "a"
)

def create_vendor_summary(conn):
    '''this function will merge the different tables to get the overall vendor summary and adding new column in the resultant data'''
vendor_salary_summary = pd.read_sql_query("""
WITH FreightSummary AS (
    SELECT
        VendorNumber,
        SUM(Freight) AS FreightCost
    FROM vendor_invoice
    GROUP BY VendorNumber
),

PurchaseSummary AS (
    SELECT 
        p.VendorNumber,
        p.VendorName,
        p.Brand,
        p.Description,
        p.PurchasePrice,
        pp.Price AS ActualPrice,
        pp.Volume,
        SUM(Quantity) AS TotalPurchaseQuantity,
        SUM(Dollars) AS TotalPurchaseDollars
    FROM purchases p
    JOIN purchase_prices pp
        ON p.Brand = pp.Brand
    WHERE p.PurchasePrice > 0
    GROUP BY 
        p.VendorNumber,
        p.VendorName,
        p.Brand,
        p.Description,
        p.PurchasePrice,
        pp.Price,
        pp.Volume
),

SalesSummary AS (
    SELECT 
        VendorNo,
        Brand,
        SUM(SalesDollars) AS TotalSalesDollars,
        SUM(SalesQuantity) AS TotalSalesQuantity,
        SUM(SalesPrice) AS TotalSalesPrice,
        SUM(ExciseTax) AS TotalExciseTax
    FROM sales
    GROUP BY VendorNo, Brand
)

SELECT 
    ps.VendorNumber,
    ps.VendorName,
    ps.Brand,
    ps.Description,
    ps.PurchasePrice,
    ps.ActualPrice,
    ps.Volume,
    ps.TotalPurchaseQuantity,
    ps.TotalPurchaseDollars,
    ss.TotalSalesDollars,
    ss.TotalSalesQuantity,
    ss.TotalSalesPrice,
    ss.TotalExciseTax,
    fs.FreightCost
FROM PurchaseSummary ps
LEFT JOIN SalesSummary ss
    ON ps.VendorNumber = ss.VendorNo
    AND ps.Brand = ss.Brand
LEFT JOIN FreightSummary fs
    ON ps.VendorNumber = fs.VendorNumber
ORDER BY ps.TotalPurchaseDollars DESC""", conn)

return vendor_sales_summary

def clean_data(df):
    '''this function will clean the data'''
    # changing datatype to float
    df['Volume'] = df['Volume'].astype('float64')

    # filtering missing value
    df.fillna(0, inplace = True)

    # reciving from categorial column
    
df['VendorName'] = df['VendorName'].str.strip()
df['Description'] = df['Description'].str.strip()

# creating new column for better analysis
vendor_salary_summary['GrossProfit'] =vendor_salary_summary['TotalSalesDollars'] - vendor_salary_summary['TotalPurchaseDollars']
vendor_salary_summary['ProfitMargin'] = vendor_salary_summary['GrossProfit'] / vendor_salary_summary['TotalSalesDollars']*100

vendor_salary_summary['StackTurnover'] = vendor_salary_summary['TotalSalesQuantity']/vendor_salary_summary['TotalPurchaseQuantity']

vendor_salary_summary['SalestoPurchaseRatio'] = vendor_salary_summary['TotalSalesDollars']/vendor_salary_summary['TotalPurchaseDollars']

return df

if __name__ == "__main__":
    load_raw_data(folder)
    # creating database connection
    conn = sqlite.connect('inventory.db')

    logging.into('creating vendor summary table....')
    summary_df = create_vendor_summary(conn)
    logging.into(summary_df.head())

    logging.into('cleaning data....')
    clean_df = clean_data(summary_df)
    logging.into(clean_df.head())


    logging.into('insert data....')
    ingest_df (clean_df.vendor_sales_summary(conn)
    logging.into('completed')

    


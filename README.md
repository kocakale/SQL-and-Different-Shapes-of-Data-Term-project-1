# SQL-and-Different-Shapes-of-Data-Term-project-1
# Term1 Data Engineering Project

## Overview

This project involves creating a MySQL database for storing and analyzing S&P 500 companies' stock data. The project includes SQL scripts for setting up the database schema, ETL procedures, and documentation.

## Project Structure

The project is organized into the following components:

- **SQL Script:**
  - `sql_code_S&P500_stocks.sql`: SQL script for creating the necessary tables,ETL procedures for importing and transforming data and creating views as data marts
  - `README.md`: Documentation file (you are currently reading it).

- **Python Script:**
  - `import_data.py`: Python script for importing stock data using the yfinance library.

## Database Schema

The database schema includes the following tables:

- `Dividends`: Stores dividend data with columns `Symbol` and `AnnualDiv`.
- `StockPrices`: Stores stock price data with columns `Date`, `Open`, `High`, `Low`, `Close`, `Adj_Close`, `Volume`, and `Symbol`.
- `Companies`: Stores information about S&P 500 companies with columns such as `CompanyID`, `Name`, `Sector`, etc.
- `CombinedAnalytics`: Analytical table with columns from `StockPrices` and additional columns like `Daily_Return`.

## Instructions for Reproduction

### 1. Database Setup

Execute `create_tables.sql` to create the necessary tables, ETL procedures and views as data marts in MySQL.

### 2. Python Data Import

1. Ensure you have Python installed on your system.
2. Install the required Python packages using: `pip install -r requirements.txt`
3. Run `import_data.py` to import data using the yfinance library.

### 3. Reproduce Project

1. Clone the repository: `git clone https://github.com/kocakale/SQL-and-Different-Shapes-of-Data-Term-project-1.git`
2. Follow the database setup and Python data import instructions.
3. Ensure MySQL server is running and accessible.

## Notes

- Make sure to configure your MySQL connection parameters in the scripts.
- The project assumes you have the necessary permissions to create databases, tables, and procedures.
- Adjust file paths and database credentials based on your local setup.


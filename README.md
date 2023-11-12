# SQL-and-Different-Shapes-of-Data-Term-project-1
# Data Engineering Project

## Overview

This project involves creating a MySQL database for storing and analyzing S&P 500 companies' stock data. The project includes SQL scripts for setting up the database schema, ETL procedures, and documentation.

Collects data about S&P 500 companies from Yahoo Finance with `yfinance` library. With Python preprocesses the data, removing unwanted entries and handling missing values. 

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
- `NetIncomes`: Stores net income data with columns `Symbol` and `NetIncome`.
- `Companies`: Stores information about S&P 500 companies with columns such as `CompanyID`, `Name`, `Sector`, etc.
- `CombinedAnalytics`: Analytical table with columns from `StockPrices`, `Dividends`, `NetIncomes` and additional columns like `Daily_Return`.

The database schema includes the following views:
- `StockPricesWithReturns`: With this view, you can retrieve stock prices along with their corresponding daily returns, enabling you to analyze the day-to-day performance of each stock in the dataset
- `vw_sector_netincome_summary`: This view provides a summary of total net income for each sector, allowing you to analyze the overall financial performance across different industry sectors
- `vw_sector_netincome_summary`: This view essentially combines net income information with company details, providing a holistic view that includes both financial data and contextual information about the companies.

There are also an event and a trigger for to periodically refresh the materialized view.

Business Questions Answered:
- `Company Analysis`: Analyzed the net income performance of individual companies.
- `Sector Analysis`: Examined total net income for different sectors in the S&P 500.
- `Dividend Yield Analysis`: Evaluated dividend yield for top companies based on stock prices and dividends.
These steps and queries collectively support business decision-making, financial analysis, and investment strategies for S&P 500 companies. The process involves data collection, storage, transformation, and the creation of analytical layers to extract valuable insights.

## Instructions for Reproduction

### 1. Database Setup

Execute `sql_code_S&P500_stocks.sql` to create the necessary tables, ETL procedures and views as data marts in MySQL.

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


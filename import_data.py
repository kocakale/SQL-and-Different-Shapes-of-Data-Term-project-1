import pandas as pd
import yfinance as yf
import mysql.connector
from mysql.connector import Error

# MySQL connection
try:
    connection = mysql.connector.connect(user='root', 
                                         password='Python23',
                                         host='localhost',
                                         database='stocks_database')
    if connection.is_connected():
        print("Connection to MySQL is succesful!")
except Error as e:
    print("Error while connecting to MySQL", e)

cursor = connection.cursor()

drop_query = """ DROP DATABASE IF EXISTS stocks_database;"""
cursor.execute(drop_query)


create_query2 = """CREATE DATABASE stocks_database;"""
cursor.execute(create_query2)


create_query3 = """USE stocks_database;"""
cursor.execute(create_query3)

create_query4 = """  CREATE TABLE Companies (
                     CompanyID VARCHAR(255) PRIMARY KEY,
                     Name VARCHAR(255),
                     Sector VARCHAR(255),
                     Industry VARCHAR(255),
                     Location VARCHAR(255),
                     DateAdded DATE,
                     CIK VARCHAR(255),
                     Founded YEAR,
                     INDEX idx_symbol (CompanyID)
                );"""
cursor.execute(create_query4)


create_query5 = """ CREATE TABLE StockPrices (
                    Date DATE,
                    Open FLOAT,
                    High FLOAT,
                    Low FLOAT,
                    Close FLOAT,
                    Adj_Close FLOAT,
                    Volume BIGINT,
                    Symbol VARCHAR(255),
                   FOREIGN KEY (Symbol) REFERENCES Companies(CompanyId)
                );"""

cursor.execute(create_query5)


create_query6 = """ CREATE TABLE Dividends (
                    Symbol VARCHAR(255),
                    AnnualDiv FLOAT,
                    FOREIGN KEY (Symbol) REFERENCES Companies(CompanyId)
                );"""
cursor.execute(create_query6)


create_query7 = """  CREATE TABLE NetIncomes (
                     Symbol VARCHAR(255),
                     NetIncome BIGINT,
                     FOREIGN KEY (Symbol) REFERENCES Companies(CompanyId)
                );"""
cursor.execute(create_query7)



# S&P 500 companies
companies = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
table  = companies[0]
#the below code removes tickers that have no data
df = table[table["Symbol"].str.contains("BRK.B|BF.B") == False]
df = df[(df.Symbol != 'SRE')&(df.Symbol != 'ES')]
df.dropna(subset=['Date added'], how='all', inplace=True)

symbols = df['Symbol'].to_list()
company_names = df['Security'].to_list()
sectors = df['GICS Sector'].to_list()
sub_industries = df['GICS Sub-Industry'].to_list()
headquarter_locations = df['Headquarters Location'].to_list()
date_added_to_index = df['Date added'].to_list()
cik_codes = df['CIK'].to_list()
company_foundation_years = df['Founded'].to_list()
company_foundation_years = [element[:4] for element in company_foundation_years]
company_foundation_years = [ int(x) for x in company_foundation_years]
company_foundation_years = [1902 if i<1902 else i for i in company_foundation_years]

# Loading companies into Companies table
for i in range(len(df)):
    insert_query = f"""INSERT INTO Companies (CompanyID, Name, Sector, Industry, Location, DateAdded, CIK, Founded) 
                       VALUES ("{symbols[i]}", "{company_names[i]}", "{sectors[i]}",
                              "{sub_industries[i]}", "{headquarter_locations[i]}", "{date_added_to_index[i]}",
                              "{cik_codes[i]}", {company_foundation_years[i]});"""
    cursor.execute(insert_query)

# Fetching stock price data and inserting into StockPrices table
for j in symbols:
    data = yf.download(j, start='2023-11-01', end='2023-11-08')
    for index, row in data.iterrows():
        insert_query = f"""INSERT INTO StockPrices (Date, Open, High, Low, Close, Adj_Close, Volume, Symbol) 
                           VALUES ('{index.strftime('%Y-%m-%d')}', {row['Open']}, {row['High']}, {row['Low']}, {row['Close']}, {row['Adj Close']}, {row['Volume']}, '{j}');"""
        cursor.execute(insert_query)
        
# Download the dividends for each symbol and concatenate the results
dfs = []
for symbol in symbols:
    stock = yf.Ticker(symbol)
    dividends = stock.history(start='2023-01-01', end='2023-11-08')["Dividends"].to_frame(name=symbol)
    dfs.append(dividends)
#drop columns with NaN and/or zero values 
df = pd.concat(dfs, axis=1).dropna(axis=1, how='all')
df = df.loc[:, (df != 0).any(axis=0)]
df.index.name = "Date"

#add 'Annual Dividend' as the last row 

df.loc['Annual Dividend'] = df.sum(axis=0)

#create a new frame with with 'Annual Dividend' row only

annual_div = df.loc['Annual Dividend'].to_frame()

# Loading dividends into Dividends table

for i, row in annual_div.iterrows():
   
    insert_query = f"""INSERT INTO Dividends (Symbol, AnnualDiv) 
                       VALUES ("{i}", "{row['Annual Dividend']}");"""
    cursor.execute(insert_query)
    
    print(f"{i} with {row['Annual Dividend']} annual dividend insterted!")
    
    
# Download the analyst recommendations for each symbol and concatenate the results

net_income_df = pd.DataFrame(index=symbols)
non_available_income_count = 0

for symbol in symbols:
    try:
        net_income = yf.Ticker(symbol).incomestmt.loc['Net Income', pd.to_datetime('2022-12-31')]
        temp_df = pd.DataFrame({symbol: net_income}, index=['net_income']).T
        net_income_df = pd.concat([net_income_df, temp_df])
   
    except Exception as e:
        print(f"Error processing key {symbol}: {e}")
        non_available_income_count += 1
        continue  # Continue to the next iteration even if an error occurs
net_income_df = net_income_df.dropna()

# Loading dividends into Dividends table

for i, row in net_income_df.iterrows():
   
   try: 
       insert_query = f"""INSERT INTO NetIncomes (Symbol, NetIncome) 
                       VALUES ("{i}", "{row['net_income']}");"""
       cursor.execute(insert_query)
       print(f"{i} with {row['net_income']} net income insterted!")
    
   except:
       continue
   
# Committing the transaction and closing the connection
connection.commit()
cursor.close()
connection.close()

import pandas as pd
import yfinance as yf
import mysql.connector
from mysql.connector import Error

# MySQL connection
try:
    connection = mysql.connector.connect(user='root', 
                                         password='Python23',
                                         host='localhost',
                                         database='yahoo_stocks')
    if connection.is_connected():
        print("Connection to MySQL is succesful!")
except Error as e:
    print("Error while connecting to MySQL", e)

cursor = connection.cursor()

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
    # Escape single quotes in the company name
    # company_name = company[1].replace("'", "''")
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
    # Escape single quotes in the company name
    # company_name = company[1].replace("'", "''")
    insert_query = f"""INSERT INTO Dividends (Symbol, AnnualDiv) 
                       VALUES ("{i}", "{row['Annual Dividend']}");"""
    cursor.execute(insert_query)

# Committing the transaction and closing the connection
connection.commit()
cursor.close()
connection.close()

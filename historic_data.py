import pandas as pd
import numpy as np
import yfinance as yf
import sqlite3
from RelevantPairs import GetRelevantPairs,FillerDataFrames,ListCorrection




def UpdateHistoricData(path):
    # Connect to the database
    conn = sqlite3.connect('tick_data2.db')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # List of table names
    table_names = ['tick_data2']

    # Loop through the tables and truncate them
    for table_name in table_names:
        # Construct and execute an SQL command to delete all rows in the table
        truncate_query = f'DELETE FROM {table_name}'
        cursor.execute(truncate_query)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    ValidPairs,correlation=FillerDataFrames(path)

    symbol_list=(ListCorrection(GetRelevantPairs(correlation,0.05,ValidPairs)))
    modified_list=[item + ".NS" for item in symbol_list]




    df=yf.download(tickers=modified_list,interval='2m',period='3d')['Close']
    df=df.dropna()
    df-df.dropna(axis=1)
    columns_to_rename = modified_list
    # Rename the columns
    for old_column_name in columns_to_rename:
        symbol = old_column_name.replace('.NS', '')  # Extract the symbol
        new_column_name = f'{symbol}'
        df = df.rename(columns={old_column_name: new_column_name})

    print(len(df),df.columns)
    df=df.tz_localize(None)
    df=df.reset_index()
    df=df.tail(30)
    conn = sqlite3.connect("tick_data2.db")

    df.to_sql("tick_data", conn, if_exists="replace", index=False)
    
    print('DB updated') 
    return symbol_list
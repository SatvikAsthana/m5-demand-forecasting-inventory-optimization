# import pandas as pd
# import numpy as np

# def load_sales_data(path):
#     print("Loading sales data...")
#     df = pd.read_csv(path)
#     print(f"Shape: {df.shape}")
#     return df

# def load_calendar_data(path):
#     print("Loading calendar data...")
#     cal = pd.read_csv(path, parse_dates=['date'])
#     print(f"Shape: {cal.shape}")
#     return cal

# def melt_sales(df):
#     print("Melting sales data to long format...")
    
#     id_vars = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']
#     value_vars = [col for col in df.columns if col.startswith('d_')]
    
#     df_long = df.melt(
#         id_vars=id_vars,
#         value_vars=value_vars,
#         var_name='d',
#         value_name='units_sold'
#     )
    
#     print(f"Long format shape: {df_long.shape}")
#     return df_long


import mysql.connector

def load_weekly_to_mysql(df):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD",
        database="m5_retail"
    )

    cursor = conn.cursor()

    insert_query = """
    INSERT INTO sales_weekly (item_id, store_id, wm_yr_wk, units_sold)
    VALUES (%s, %s, %s, %s)
    """

    data = list(df.itertuples(index=False, name=None))
    cursor.executemany(insert_query, data)

    conn.commit()
    cursor.close()
    conn.close()

    print("Data loaded into MySQL.")

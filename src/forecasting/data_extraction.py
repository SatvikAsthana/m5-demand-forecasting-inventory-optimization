import mysql.connector
import pandas as pd


def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="satvik0201",
        database="m5_retail"
    )


def extract_a_class_weekly_data():
    conn = get_connection()

    query = """
   SELECT 
    sw.item_id,
    sw.store_id,
    sw.wm_yr_wk,
    sw.units_sold,

    -- Price
    sp.sell_price,

    -- Calendar basics
    c.month,
    c.wday,

    -- Events
    c.event_name_1,
    c.event_type_1,
    c.event_name_2,
    c.event_type_2,

    -- SNAP flags
    c.snap_CA,
    c.snap_TX,
    c.snap_WI

FROM sales_weekly sw

JOIN sku_cumulative sc
    ON sw.item_id = sc.item_id
   AND sw.store_id = sc.store_id

JOIN calendar c
    ON sw.wm_yr_wk = c.wm_yr_wk

LEFT JOIN sell_prices sp
    ON sw.item_id = sp.item_id
   AND sw.store_id = sp.store_id
   AND sw.wm_yr_wk = sp.wm_yr_wk

WHERE sc.abc_class = 'A';



"""


    df = pd.read_sql(query, conn)
    conn.close()

    print("Extracted rows:", df.shape)
    return df


if __name__ == "__main__":
    df = extract_a_class_weekly_data()
    print(df.head())

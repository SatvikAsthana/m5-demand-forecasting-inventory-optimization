CREATE DATABASE IF NOT EXISTS m5_retail;
USE m5_retail;

CREATE TABLE sales_weekly (
    item_id VARCHAR(50),
    store_id VARCHAR(10),
    wm_yr_wk INT,
    units_sold INT,
    PRIMARY KEY (item_id, store_id, wm_yr_wk)
);

CREATE TABLE sell_prices (
    store_id VARCHAR(10),
    item_id VARCHAR(50),
    wm_yr_wk INT,
    sell_price FLOAT,
    PRIMARY KEY (store_id, item_id, wm_yr_wk)
);

LOAD DATA LOCAL INFILE 
'C:/Users/Satvik Asthana/OneDrive/Desktop/M5 Demand Forecasting Inventory Optimization/data/raw/sell_prices.csv'
INTO TABLE sell_prices
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(store_id, item_id, wm_yr_wk, sell_price);


CREATE TABLE calendar (
    date DATE,
    wm_yr_wk INT,
    weekday VARCHAR(10),
    wday INT,
    month INT,
    year INT,
    event_name_1 VARCHAR(50),
    event_type_1 VARCHAR(50),
    event_name_2 VARCHAR(50),
    event_type_2 VARCHAR(50),
    snap_CA INT,
    snap_TX INT,
    snap_WI INT
);

LOAD DATA LOCAL INFILE 
'C:/Users/Satvik Asthana/OneDrive/Desktop/M5 Demand Forecasting Inventory Optimization/data/raw/calendar.csv'
INTO TABLE calendar
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT COUNT(*) FROM calendar;

SHOW WARNINGS;

CREATE DATABASE IF NOT EXISTS m5_retail;
USE m5_retail;

CREATE TABLE sales_weekly (
    item_id VARCHAR(50),
    store_id VARCHAR(10),
    wm_yr_wk INT,
    units_sold INT,
    PRIMARY KEY (item_id, store_id, wm_yr_wk)
);

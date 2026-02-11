CREATE TABLE sku_demand_stats AS
SELECT
    item_id,
    store_id,
    AVG(units_sold) AS avg_weekly_demand,
    STDDEV(units_sold) AS std_weekly_demand,
    COUNT(*) AS weeks_observed
FROM sales_weekly
GROUP BY item_id, store_id;

ALTER TABLE sku_demand_stats
ADD COLUMN cv DOUBLE;

UPDATE sku_demand_stats
SET cv = std_weekly_demand / NULLIF(avg_weekly_demand, 0);

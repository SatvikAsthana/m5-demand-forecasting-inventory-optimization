CREATE TABLE sku_total_demand AS
SELECT
    item_id,
    store_id,
    SUM(avg_weekly_demand) AS total_avg_demand
FROM sku_demand_stats
GROUP BY item_id, store_id;

CREATE TABLE sku_ranked AS
SELECT
    item_id,
    store_id,
    total_avg_demand,
    RANK() OVER (ORDER BY total_avg_demand DESC) AS demand_rank
FROM sku_total_demand;

CREATE TABLE sku_cumulative AS
SELECT
    item_id,
    store_id,
    total_avg_demand,
    demand_rank,
    SUM(total_avg_demand) OVER (ORDER BY total_avg_demand DESC)
        / SUM(total_avg_demand) OVER () AS cumulative_share
FROM sku_ranked;

ALTER TABLE sku_cumulative
ADD COLUMN abc_class VARCHAR(1);

SET SQL_SAFE_UPDATES = 0;

UPDATE sku_cumulative
SET abc_class =
    CASE
        WHEN cumulative_share <= 0.80 THEN 'A'
        WHEN cumulative_share <= 0.95 THEN 'B'
        ELSE 'C'
    END;

SET SQL_SAFE_UPDATES = 1;

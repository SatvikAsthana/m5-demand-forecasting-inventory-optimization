USE m5_retail;

-- Join ABC classification with coefficient of variation
CREATE TABLE sku_profile AS
SELECT 
    c.item_id,
    c.store_id,
    c.total_avg_demand,
    s.cv,
    c.abc_class
FROM sku_cumulative c
JOIN sku_demand_stats s
    ON c.item_id = s.item_id
    AND c.store_id = s.store_id;

-- Volatility summary by ABC class
SELECT 
    abc_class,
    ROUND(AVG(cv), 2) AS avg_cv,
    ROUND(MAX(cv), 2) AS max_cv,
    COUNT(*) AS sku_count
FROM sku_profile
GROUP BY abc_class;

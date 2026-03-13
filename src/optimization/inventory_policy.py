import numpy as np
import pandas as pd
from scipy.stats import norm

from services.forecast_service import get_trained_forecast


def build_inventory_policy(
    service_level=0.95,
    lead_time=2,
    holding_cost=2,
    order_cost=50,
    stockout_penalty=20,   # ← now a real parameter, not hardcoded
):
    print(f"Running inventory policy | SL={service_level} | LT={lead_time} | HC={holding_cost} | OC={order_cost}")

    # ── 1. Forecast ──────────────────────────────────────────────────────────
    model, df, features = get_trained_forecast()
    df["forecast"] = model.predict(df[features])

    # ── 2. Per-SKU demand stats ───────────────────────────────────────────────
    sku_stats = (
        df.groupby(["item_id", "store_id"])
        .agg(avg_demand=("forecast", "mean"), demand_std=("forecast", "std"))
        .reset_index()
    )

    # ── 3. Lead-time statistics ───────────────────────────────────────────────
    sku_stats["demand_during_lead"] = sku_stats["avg_demand"] * lead_time
    sku_stats["std_during_lead"]    = sku_stats["demand_std"] * np.sqrt(lead_time)

    # ── 4. Z-score & safety stock ────────────────────────────────────────────
    Z = norm.ppf(service_level)
    print(f"  Z-score: {Z:.4f}")

    sku_stats["safety_stock"]  = Z * sku_stats["std_during_lead"]
    sku_stats["reorder_point"] = sku_stats["demand_during_lead"] + sku_stats["safety_stock"]

    # ── 5. EOQ ───────────────────────────────────────────────────────────────
    annual_demand      = sku_stats["avg_demand"] * 52
    sku_stats["eoq"]   = np.sqrt((2 * annual_demand * order_cost) / holding_cost)

    # ── 6. Holding cost  (cycle stock + safety stock) ────────────────────────
    avg_inventory              = sku_stats["eoq"] / 2 + sku_stats["safety_stock"]
    sku_stats["holding_cost"]  = avg_inventory * holding_cost

    # ── 7. Ordering cost ─────────────────────────────────────────────────────
    sku_stats["ordering_cost"] = (annual_demand / sku_stats["eoq"]) * order_cost

    # ── 8. Stockout cost via the standard normal loss function ───────────────
    #   L(Z) = φ(Z) − Z · (1 − Φ(Z))      ← single, correct definition
    Lz = norm.pdf(Z) - Z * (1 - norm.cdf(Z))

    sku_stats["expected_shortage"] = sku_stats["std_during_lead"] * Lz
    sku_stats["annual_shortage"]   = (
        sku_stats["expected_shortage"] * (annual_demand / sku_stats["eoq"])
    )
    sku_stats["stockout_cost"] = sku_stats["annual_shortage"] * stockout_penalty

    print(f"  Annual shortage sum : {sku_stats['annual_shortage'].sum():.2f}")
    print(f"  Stockout cost sum   : {sku_stats['stockout_cost'].sum():.2f}")

    # ── 9. Total cost ────────────────────────────────────────────────────────
    sku_stats["total_cost"] = (
        sku_stats["holding_cost"]
        + sku_stats["ordering_cost"]
        + sku_stats["stockout_cost"]
    )

    print("\nInventory Policy Sample:")
    print(sku_stats.head())

    return sku_stats


if __name__ == "__main__":
    build_inventory_policy(service_level=0.99)

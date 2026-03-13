import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd
from optimization.inventory_policy import build_inventory_policy


def load_inventory_data(service_level, lead_time, holding_cost, order_cost, stockout_penalty=20):
    """Build inventory policy for the given parameter set."""
    df = build_inventory_policy(
        service_level=service_level,
        lead_time=lead_time,
        holding_cost=holding_cost,
        order_cost=order_cost,
        stockout_penalty=stockout_penalty,
    )
    return df


def compute_kpis(df: pd.DataFrame) -> dict:
    """Compute executive-level KPIs from a policy dataframe."""
    return {
        "total_skus":        len(df),
        "avg_safety_stock":  df["safety_stock"].mean(),
        "avg_reorder_point": df["reorder_point"].mean(),
        "total_cost":        df["total_cost"].sum(),
        "avg_cost_per_sku":  df["total_cost"].mean(),
    }

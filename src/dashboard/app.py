import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import norm

from services.dashboard_service import load_inventory_data, compute_kpis

st.set_page_config(layout="wide")
st.title("📦 M5 Demand Forecasting & Inventory Optimization")

# ── Sidebar controls ──────────────────────────────────────────────────────────
st.sidebar.header("Simulation Controls")

service_level    = st.sidebar.slider("Service Level",     0.80, 0.99, 0.95)
lead_time        = st.sidebar.slider("Lead Time (weeks)", 1,    8,    2)
holding_cost     = st.sidebar.slider("Holding Cost",      1,    10,   2)
order_cost       = st.sidebar.slider("Order Cost",        10,   200,  50)
stockout_penalty = st.sidebar.slider("Stockout Penalty",  1,    100,  20)

# ── Load data ─────────────────────────────────────────────────────────────────
df = load_inventory_data(
    service_level=service_level,
    lead_time=lead_time,
    holding_cost=holding_cost,
    order_cost=order_cost,
    stockout_penalty=stockout_penalty,
)

kpis = compute_kpis(df)

# ── KPI metrics ───────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total SKUs",        kpis["total_skus"])
col2.metric("Avg Safety Stock",  round(kpis["avg_safety_stock"],  2))
col3.metric("Avg Reorder Point", round(kpis["avg_reorder_point"], 2))
col4.metric("Total Cost",        round(kpis["total_cost"],        2))

st.divider()

# ── Policy sample table ───────────────────────────────────────────────────────
st.subheader("Inventory Policy Sample")
st.dataframe(df.head(50))

st.divider()

# ── Cost breakdown bar chart ──────────────────────────────────────────────────
st.subheader("Cost Breakdown")

cost_df = pd.DataFrame({
    "Cost Type":    ["Holding Cost", "Ordering Cost", "Stockout Cost"],
    "Total Amount": [
        df["holding_cost"].sum(),
        df["ordering_cost"].sum(),
        df["stockout_cost"].sum(),
    ],
}).set_index("Cost Type")

st.bar_chart(cost_df)

st.divider()

# ── Top 10 most expensive SKUs ────────────────────────────────────────────────
st.subheader("Top 10 SKUs by Total Cost")
top_skus = df.sort_values("total_cost", ascending=False).head(10)
st.dataframe(top_skus[[
    "item_id", "store_id", "total_cost", "safety_stock", "reorder_point"
]])

st.divider()

# ── Service-level sensitivity analysis ───────────────────────────────────────
st.subheader("Service Level vs Total Cost")

# ── Debug expander — shows your data scale so you can tune sliders ────────────
with st.expander("🔍 Debug: Data Scale Info"):
    cycle_stock_mean = (df["eoq"] / 2).mean()
    safety_stock_mean = df["safety_stock"].mean()
    ratio = safety_stock_mean / cycle_stock_mean if cycle_stock_mean > 0 else 0
    st.write(f"avg_demand mean       : {df['avg_demand'].mean():.4f}")
    st.write(f"demand_std mean       : {df['demand_std'].mean():.4f}")
    st.write(f"std_during_lead mean  : {df['std_during_lead'].mean():.4f}")
    st.write(f"eoq mean              : {df['eoq'].mean():.4f}")
    st.write(f"cycle_stock mean      : {cycle_stock_mean:.4f}")
    st.write(f"safety_stock mean     : {safety_stock_mean:.4f}")
    st.write(f"safety / cycle ratio  : {ratio:.4f}  ← needs to be > 0.05 for U-shape")

# ── Pre-compute fixed values ──────────────────────────────────────────────────
annual_demand = df["avg_demand"] * 52
eoq           = df["eoq"]
cycle_stock   = eoq / 2
std_lead      = df["std_during_lead"]

service_levels     = np.linspace(0.80, 0.99, 20)
sensitivity_results = []

for sl in service_levels:
    Z  = norm.ppf(sl)
    Lz = norm.pdf(Z) - Z * (1 - norm.cdf(Z))   # standard normal loss function

    safety_stock = Z * std_lead

    # Holding: cycle stock + safety stock, multiplied by holding cost per unit
    h_cost = (cycle_stock + safety_stock) * holding_cost

    # Ordering: independent of service level
    o_cost = (annual_demand / eoq) * order_cost

    # Stockout: expected shortage per cycle × cycles per year × penalty
    expected_shortage = std_lead * Lz
    annual_shortage   = expected_shortage * (annual_demand / eoq)
    s_cost            = annual_shortage * stockout_penalty

    total = (h_cost + o_cost + s_cost).sum()

    sensitivity_results.append({
        "service_level": round(sl, 4),
        "total_cost":    round(total, 2),
        "holding":       round(h_cost.sum(), 2),
        "ordering":      round(o_cost.sum(), 2),
        "stockout":      round(s_cost.sum(), 2),
    })

sensitivity_df = pd.DataFrame(sensitivity_results).set_index("service_level")

# ── Optimal service level ─────────────────────────────────────────────────────
optimal_sl   = sensitivity_df["total_cost"].idxmin()
optimal_cost = sensitivity_df["total_cost"].min()
st.success(f"✅ Optimal Service Level: **{optimal_sl}**  —  Minimum Total Cost: **{optimal_cost:,.0f}**")

# ── Plot ──────────────────────────────────────────────────────────────────────
st.line_chart(sensitivity_df[["holding", "ordering", "stockout", "total_cost"]])

# ── Smart warning if U-shape won't appear ─────────────────────────────────────
h_at_80 = sensitivity_df["holding"].iloc[0]
h_at_99 = sensitivity_df["holding"].iloc[-1]
s_at_80 = sensitivity_df["stockout"].iloc[0]
h_rise  = h_at_99 - h_at_80

if s_at_80 < h_rise:
    # Suggest a penalty that would make stockout at SL=0.80 equal to h_rise × 1.5
    raw_stockout_at_80 = s_at_80 / stockout_penalty if stockout_penalty > 0 else 1
    suggested = min(int((h_rise * 1.5) / max(raw_stockout_at_80, 1)), 100)
    st.warning(
        f"⚠️ U-shape not visible: holding cost rises by {h_rise:,.0f} across the range, "
        f"but stockout cost at SL=0.80 is only {s_at_80:,.0f}. "
        f"Try raising **Stockout Penalty** to ~**{suggested}** to balance them."
    )
else:
    st.info("✅ Stockout and holding costs are balanced — U-shape should be visible.")

st.caption(
    "Holding cost rises with service level (more safety stock). "
    "Stockout cost falls as fewer shortages occur. "
    "The minimum of the total cost curve is the optimal service level."
)
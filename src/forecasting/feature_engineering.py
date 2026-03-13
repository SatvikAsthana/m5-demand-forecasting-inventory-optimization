import pandas as pd
import numpy as np


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create lag, rolling, pricing, event, seasonal and trend features.
    Memory-safe implementation (no high-cardinality one-hot encoding).
    """

    # -----------------------------
    # Sort properly
    # -----------------------------
    df = df.sort_values(["item_id", "store_id", "wm_yr_wk"])

    group_cols = ["item_id", "store_id"]

    # -----------------------------
    # LAG FEATURES
    # -----------------------------
    for lag in [1, 2, 3, 4, 6, 12, 52]:
        df[f"lag_{lag}"] = df.groupby(group_cols)["units_sold"].shift(lag)

    # -----------------------------
    # ROLLING FEATURES
    # -----------------------------
    for window in [4, 8, 12, 26]:
        df[f"rolling_mean_{window}"] = (
            df.groupby(group_cols)["units_sold"]
            .shift(1)
            .rolling(window)
            .mean()
        )

        df[f"rolling_std_{window}"] = (
            df.groupby(group_cols)["units_sold"]
            .shift(1)
            .rolling(window)
            .std()
        )

    # -----------------------------
    # PRICE FEATURES
    # -----------------------------
    df["price_change"] = (
        df.groupby(group_cols)["sell_price"]
        .pct_change()
    )

    df["rolling_price_mean_4"] = (
        df.groupby(group_cols)["sell_price"]
        .shift(1)
        .rolling(4)
        .mean()
    )

    df["rolling_price_std_4"] = (
        df.groupby(group_cols)["sell_price"]
        .shift(1)
        .rolling(4)
        .std()
    )

    # -----------------------------
    # SNAP AGGREGATION
    # -----------------------------
    if {"snap_CA", "snap_TX", "snap_WI"}.issubset(df.columns):
        df["snap_flag"] = df[["snap_CA", "snap_TX", "snap_WI"]].max(axis=1)
    else:
        df["snap_flag"] = 0

    # -----------------------------
    # EVENT FEATURES (Memory Safe)
    # -----------------------------
    event_cols = [
        "event_name_1",
        "event_type_1",
        "event_name_2",
        "event_type_2"
    ]

    existing_event_cols = [col for col in event_cols if col in df.columns]

    if existing_event_cols:

        df["has_event"] = 0

        if "event_name_1" in df.columns:
            df["has_event"] |= df["event_name_1"].notna()

        if "event_name_2" in df.columns:
            df["has_event"] |= df["event_name_2"].notna()

        df["has_event"] = df["has_event"].astype(int)

        # Drop high-cardinality event columns
        df = df.drop(columns=existing_event_cols)

    else:
        df["has_event"] = 0

    # -----------------------------
    # TREND FEATURE
    # -----------------------------
    if {"rolling_mean_4", "rolling_mean_12"}.issubset(df.columns):
        df["trend_4_12"] = df["rolling_mean_4"] - df["rolling_mean_12"]
    else:
        df["trend_4_12"] = 0

    # -----------------------------
    # SEASONAL ENCODING
    # -----------------------------
    if "wm_yr_wk" in df.columns:
        df["week_mod_52"] = df["wm_yr_wk"] % 100

        df["week_sin"] = np.sin(
            2 * np.pi * df["week_mod_52"] / 52
        )

        df["week_cos"] = np.cos(
            2 * np.pi * df["week_mod_52"] / 52
        )
    else:
        df["week_mod_52"] = 0
        df["week_sin"] = 0
        df["week_cos"] = 0

    # -----------------------------
    # ONE-HOT MONTH ONLY
    # -----------------------------
    if "month" in df.columns:
        df = pd.get_dummies(
            df,
            columns=["month"],
            drop_first=True
        )

    # -----------------------------
    # DROP NA (from lag creation)
    # -----------------------------
    df = df.dropna().copy()

    return df

import pandas as pd
import numpy as np


def create_features(df):

    # Sort properly
    df = df.sort_values(["item_id", "store_id", "wm_yr_wk"])

    group_cols = ["item_id", "store_id"]

    # ---------------------------
    # LAG FEATURES
    # ---------------------------
    for lag in [1, 2, 3, 4, 6, 12, 52]:
        df[f"lag_{lag}"] = df.groupby(group_cols)["units_sold"].shift(lag)

    # ---------------------------
    # ROLLING FEATURES
    # ---------------------------
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
        # ---------------------------
# PRICE FEATURES
# ---------------------------
        df["price_change"] = df.groupby(["item_id", "store_id"])["sell_price"].pct_change()

        df["rolling_price_mean_4"] = (
            df.groupby(["item_id", "store_id"])["sell_price"]
            .shift(1)
            .rolling(4)
            .mean()
            )

        df["rolling_price_std_4"] = (
            df.groupby(["item_id", "store_id"])["sell_price"]
            .shift(1)
            .rolling(4)
            .std()
            )

# ---------------------------
# EVENT FEATURES
# ---------------------------
        df["has_event"] = df["event_name_1"].notnull().astype(int)

# SNAP aggregation (state-specific later possible)
        df["snap_flag"] = df[["snap_CA", "snap_TX", "snap_WI"]].max(axis=1)

# One-hot month
        print("Columns before encoding:", df.columns.tolist())
    df = pd.get_dummies(df, columns=["month"], drop_first=True)



    # ---------------------------
    # TREND FEATURE
    # ---------------------------
    df["trend_4_12"] = df["rolling_mean_4"] - df["rolling_mean_12"]

    # ---------------------------
    # SEASONAL ENCODING
    # ---------------------------
    # Extract week number within year
    df["week_mod_52"] = df["wm_yr_wk"] % 100  # assuming format YYYYWW

    df["week_sin"] = np.sin(2 * np.pi * df["week_mod_52"] / 52)
    df["week_cos"] = np.cos(2 * np.pi * df["week_mod_52"] / 52)

    # ---------------------------
    # DROP NA (from lags)
    # ---------------------------
    df = df.dropna().copy()

    return df

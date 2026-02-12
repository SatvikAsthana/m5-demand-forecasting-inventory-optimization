import pandas as pd
from data_extraction import extract_a_class_weekly_data
from feature_engineering import create_features
from sklearn.metrics import mean_absolute_error
import lightgbm as lgb
import numpy as np


def train_model():

    # Extract
    df = extract_a_class_weekly_data()

    print("Columns after extraction:")
    print(df.columns.tolist())
    
    print("Columns after extraction:", df.columns.tolist())


    # Feature engineering
    df = create_features(df)

    # Time-based split
    cutoff = sorted(df["wm_yr_wk"].unique())[-8]

    train = df[df["wm_yr_wk"] < cutoff]
    test = df[df["wm_yr_wk"] >= cutoff]

    features = [col for col in df.columns 
                if col not in ["item_id", "store_id", "wm_yr_wk", "units_sold"]]
    
    # Keep only numeric features
    numeric_cols = df[features].select_dtypes(include=["number"]).columns
    features = list(numeric_cols)


    target = "units_sold"

    X_train = train[features]
    y_train = train[target]

    X_test = test[features]
    y_test = test[target]

    model = lgb.LGBMRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=-1,
        num_leaves=64,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    print("Train size:", X_train.shape)
    print("Test size:", X_test.shape)
    print("MAE:", round(mae, 3))


if __name__ == "__main__":
    train_model()

from services.model_service import load_model
from forecasting.feature_engineering import create_features
from forecasting.data_extraction import extract_a_class_weekly_data


def get_trained_forecast():
    """
    Returns trained model, dataset, and feature list.
    This function should be called ONCE and cached at dashboard level.
    """
    model = load_model()
    df = extract_a_class_weekly_data()
    df = create_features(df)

    features = [col for col in df.columns
                if col not in ["item_id", "store_id", "wm_yr_wk", "units_sold"]]

    # Keep ONLY numeric columns (same as training)
    numeric_cols = df[features].select_dtypes(include=["number"]).columns
    features = list(numeric_cols)

    return model, df, features
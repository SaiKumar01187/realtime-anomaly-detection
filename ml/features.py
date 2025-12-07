import pandas as pd

# Columns that will be used as input to the ML model
FEATURE_COLUMNS = [
    "amount",
    "device_score",
    "ip_risk_score",
    "is_high_risk_country",
    "is_night",
]

# You can adjust this list based on your data
HIGH_RISK_COUNTRIES = {"NG", "RU", "BR"}


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Take a raw transactions DataFrame and add feature columns
    for anomaly detection.
    """

    df = df.copy()

    # Ensure timestamp is datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Hour of day
    df["hour"] = df["timestamp"].dt.hour

    # Night-time transactions (e.g., 10pm–6am)
    df["is_night"] = ((df["hour"] < 6) | (df["hour"] > 22)).astype(int)

    # High-risk country flag
    df["is_high_risk_country"] = df["country"].isin(HIGH_RISK_COUNTRIES).astype(int)

    # Make sure numeric columns are the right type
    df["amount"] = df["amount"].astype(float)
    df["device_score"] = df["device_score"].astype(float)
    df["ip_risk_score"] = df["ip_risk_score"].astype(float)

    return df

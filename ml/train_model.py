import pandas as pd
from joblib import dump
from sklearn.ensemble import IsolationForest

from features import build_features, FEATURE_COLUMNS


INPUT_PARQUET = "../data/transactions.parquet"
MODEL_PATH = "../models/isolation_forest.pkl"


def main():
    print("Loading data from:", INPUT_PARQUET)
    df = pd.read_parquet(INPUT_PARQUET)

    print("Building features...")
    df_feat = build_features(df)

    X = df_feat[FEATURE_COLUMNS]

    print("Training IsolationForest on", len(X), "rows and", X.shape[1], "features")

    model = IsolationForest(
        n_estimators=200,
        contamination=0.02,  # expected anomaly ratio, tune if needed
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X)

    print("Saving model to:", MODEL_PATH)
    dump(model, MODEL_PATH)

    print("Done! Model saved.")


if __name__ == "__main__":
    main()

import json
import pandas as pd
from pathlib import Path

DATA_PATH = Path("../data/transactions_log.jsonl")
OUTPUT_PARQUET = Path("../data/transactions.parquet")

def main():
    records = []
    with open(DATA_PATH, "r") as f:
        for line in f:
            records.append(json.loads(line))

    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # SAVE TO ROOT DATA FOLDER
    df.to_parquet(OUTPUT_PARQUET, index=False)

    print("Saved", OUTPUT_PARQUET, "with", len(df), "rows")

if __name__ == "__main__":
    main()

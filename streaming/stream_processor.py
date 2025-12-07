# streaming/python_stream_processor.py
import json
import time
from typing import List

import pandas as pd
from kafka import KafkaConsumer
from joblib import load
import psycopg2

from ml.features import build_features, FEATURE_COLUMNS

KAFKA_BOOTSTRAP = "localhost:29092"
KAFKA_TOPIC = "transactions_raw"

PG_HOST = "localhost"
PG_PORT = 5432
PG_DB = "anomalies"
PG_USER = "app"
PG_PASSWORD = "app"

MODEL_PATH = "models/isolation_forest.pkl"
THRESHOLD = 0.0
BATCH_SIZE = 100
BATCH_TIMEOUT = 5


def make_pg_conn():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD,
    )


def write_to_postgres(df: pd.DataFrame):
    if df.empty:
        return

    conn = make_pg_conn()
    cur = conn.cursor()

    rows_scored = df[
        [
            "transaction_id", "user_id", "merchant_id", "amount",
            "currency", "country", "channel", "timestamp",
            "device_score", "ip_risk_score",
            "anomaly_score", "is_anomaly",
        ]
    ].values.tolist()

    insert_tx = """
        INSERT INTO transactions_scored (
            transaction_id, user_id, merchant_id, amount,
            currency, country, channel, timestamp,
            device_score, ip_risk_score,
            anomaly_score, is_anomaly
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (transaction_id) DO NOTHING
    """

    cur.executemany(insert_tx, rows_scored)

    anomalies = df[df["is_anomaly"] == 1]
    if not anomalies.empty:
        rows_anom = anomalies[
            [
                "transaction_id", "user_id", "merchant_id", "amount",
                "currency", "country", "channel", "timestamp",
                "device_score", "ip_risk_score",
                "anomaly_score", "is_anomaly",
            ]
        ].values.tolist()

        insert_anom = """
            INSERT INTO anomalies (
                transaction_id, user_id, merchant_id, amount,
                currency, country, channel, timestamp,
                device_score, ip_risk_score,
                anomaly_score, is_anomaly
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (transaction_id) DO NOTHING
        """
        cur.executemany(insert_anom, rows_anom)

    conn.commit()
    cur.close()
    conn.close()


def main():
    print("Loading ML model...")
    model = load(MODEL_PATH)

    print("Connecting to Kafka...")
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="latest",
    )

    buffer: List[dict] = []
    last_flush = time.time()

    print("Python streaming processor started!")
    while True:
        msg_pack = consumer.poll(timeout_ms=1000)

        any_records = False
        for tp, messages in msg_pack.items():
            for message in messages:
                any_records = True
                buffer.append(message.value)

        now = time.time()
        time_up = (now - last_flush) >= BATCH_TIMEOUT

        if buffer and (len(buffer) >= BATCH_SIZE or time_up):
            print(f"Scoring batch of {len(buffer)} rows...")

            pdf = pd.DataFrame(buffer)
            pdf["timestamp"] = pd.to_datetime(pdf["timestamp"])

            feat_df = build_features(pdf)
            X = feat_df[FEATURE_COLUMNS]

            scores = model.decision_function(X)
            pdf["anomaly_score"] = scores
            pdf["is_anomaly"] = (pdf["anomaly_score"] < THRESHOLD).astype(int)

            write_to_postgres(pdf)

            print(
                f"✔ Wrote {len(pdf)} scored rows "
                f"({(pdf['is_anomaly']==1).sum()} anomalies)"
            )

            buffer.clear()
            last_flush = now

        if not any_records:
            time.sleep(1)


if __name__ == "__main__":
    main()

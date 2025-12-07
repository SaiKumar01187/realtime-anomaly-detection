<!-- PROJECT BANNER --> <p align="center"> <img src="https://dummyimage.com/1200x250/0d1117/ffffff&text=Real-Time+Anomaly+Detection+System" alt="Project Banner"/> </p> <h1 align="center">⚡ Real-Time Anomaly Detection System</h1> <p align="center"> <strong>Apache Kafka · PySpark Streaming · Machine Learning · PostgreSQL · Grafana</strong> </p> <p align="center"> <img src="https://img.shields.io/badge/Build-Passing-brightgreen?style=flat-square"/> <img src="https://img.shields.io/badge/PySpark-3.5-orange?style=flat-square"/> <img src="https://img.shields.io/badge/Kafka-Streaming-black?style=flat-square"/> <img src="https://img.shields.io/badge/Python-3.10-blue?style=flat-square"/> <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square"/> </p>
📝 Overview

This project implements a real-time anomaly & fraud detection pipeline using modern data engineering and machine learning technologies. It simulates transactions, streams them via Kafka, scores them in PySpark using an Isolation Forest model, stores results in PostgreSQL, and visualizes anomalies via Grafana.

Perfect for:
✔ Real-time streaming ML
✔ Fraud analytics
✔ Kafka–Spark pipelines
✔ Data engineering portfolio projects

## 🚀 Architecture

```text
               ┌───────────────────────┐
               │  Transaction Producer │
               │      (Python + Faker) │
               └───────────┬───────────┘
                           │
                           ▼
   ┌──────────────────────────────────────────┐
   │                  Kafka                    │
   │        Topic: transactions_raw            │
   └───────────────┬──────────────────────────┘
                   ▼
        ┌──────────────────────────────┐
        │      PySpark Streaming       │
        │  - Parse JSON                │
        │  - Build ML features         │
        │  - Apply Isolation Forest    │
        │  - Determine anomalies       │
        └───────────────┬──────────────┘
                        ▼
       ┌──────────────────────────────────┐
       │             PostgreSQL            │
       │  Tables:                          │
       │   - transactions_scored           │
       │   - anomalies                     │
       └──────────────────┬───────────────┘
                          ▼
         ┌────────────────────────────────┐
         │             Grafana             │
         │    Real-time anomaly dashboards │
         └────────────────────────────────┘
```





## 📁 Project Structure
```text
realtime-anomaly-detection/
│
├── producer/
│   └── transaction_producer.py
│
├── streaming/
│   └── stream_processor.py
│
├── ml/
│   ├── prepare_data.py
│   ├── features.py
│   └── train_model.py
│
├── models/
│   └── isolation_forest.pkl
│
├── data/
│   ├── transactions_log.jsonl
│   └── checkpoints/
│
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Setup & Installation
1️⃣ Clone the repository
git clone https://github.com/YOUR_USERNAME/realtime-anomaly-detection.git
cd realtime-anomaly-detection

2️⃣ Create & activate virtual environment
python -m venv venv
venv\Scripts\activate         # Windows
source venv/bin/activate     # macOS/Linux

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Start Kafka + PostgreSQL using Docker
docker-compose up -d

## 🧪 Generate Training Data
# 1️⃣ Run the Transaction Generator

This script simulates real-time transactions and writes them as JSONL for training.
```text
┌─────────────────────────────┐
│ Transaction Generator (Py)  │
│  • Faker simulated data     │
│  • Normal + anomalous tx    │
└──────────────┬──────────────┘
               ▼
      data/transactions_log.jsonl
```


# Run:

python producer/transaction_producer.py
```text

📊 Step 2 — Convert JSONL → Parquet

Convert raw logs to Parquet for ML efficiency.

JSONL ─────▶ Parquet
```


# Run:

python ml/prepare_data.py
```text

🤖 Step 3 — Train the ML Model (Isolation Forest)
┌────────────────────────────────────┐
│     ML Training Pipeline           │
│  • Load Parquet                    │
│  • Build features                  │
│  • IsolationForest anomaly model   │
└──────────────────┬─────────────────┘
                   ▼
        models/isolation_forest.pkl
```


# Run training:

python ml/train_model.py

# 🔥 Run the Real-Time Streaming Job

This launches the PySpark pipeline that does live anomaly detection.
```text
Kafka Topic: transactions_raw
          │
          ▼
┌─────────────────────────────┐
│ PySpark Streaming Job       │
│  • Parse JSON               │
│  • Build features           │
│  • Apply ML model           │
│  • Insert results → SQL     │
└──────────────┬──────────────┘
               ▼
      PostgreSQL: anomalies table
```

# Start streaming:

python streaming/stream_processor.py

The job performs:

✓ Reads live events from Kafka

✓ Scores transactions using Isolation Forest

✓ Writes outputs to PostgreSQL

✓ Exposes anomaly metrics for Grafana

## 📈 Grafana Dashboards

<img width="900" height="600" alt="image" src="https://github.com/user-attachments/assets/60a5838d-be84-4c91-a92a-6a2873e3c1a0" />


Access Grafana:

👉 http://localhost:3000

Login: admin / admin

Example PostgreSQL query:

SELECT timestamp, is_anomaly
FROM anomalies
ORDER BY timestamp;


## 🧠 Technologies Used
```text
┌───────────────────┬──────────────────────────────────────────────┐
│ Component         │ Technology                                    │
├───────────────────┼──────────────────────────────────────────────┤
│ Streaming         │ Apache Kafka                                  │
│ Processing        │ PySpark Structured Streaming                  │
│ Machine Learning  │ Isolation Forest (scikit-learn)               │
│ Storage           │ PostgreSQL                                    │
│ Visualization     │ Grafana                                       │
│ Deployment        │ Docker Compose                                │
│ Scripting         │ Python                                        │
└───────────────────┴──────────────────────────────────────────────┘
```

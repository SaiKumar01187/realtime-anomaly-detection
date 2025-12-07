

██████╗ ███████╗ █████╗ ████████╗██╗███╗   ███╗

██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██║████╗ ████║

██████╔╝█████╗  ███████║   ██║   ██║██╔████╔██║

██╔══██╗██╔══╝  ██╔══██║   ██║   ██║██║╚██╔╝██║

██║  ██║███████╗██║  ██║   ██║   ██║██║ ╚═╝ ██║

╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝     ╚═╝



&nbsp;     REAL-TIME ANOMALY \& FRAUD DETECTION PIPELINE

&nbsp; Apache Kafka • PySpark Streaming • ML • PostgreSQL • Grafana

🚀 Real-Time Anomaly Detection System

Kafka → PySpark Streaming → ML Model → PostgreSQL → Grafana Dashboards





















📌 Overview



This project is a real-time anomaly \& fraud detection system that simulates financial transactions, processes them through a streaming ML pipeline, stores results in PostgreSQL, and visualizes anomalies in Grafana.

\# Real-Time Transaction Anomaly Detection



End-to-end demo of a real-time fraud / anomaly detection pipeline using:



\- \*\*Kafka\*\* – streaming transaction events  

\- \*\*Python / scikit-learn\*\* – feature engineering \& Isolation Forest model  

\- \*\*Streaming processor\*\* (PySpark or pure Python) – score events in real time  

\- \*\*PostgreSQL\*\* – store scored transactions \& anomalies  

\- \*\*Grafana\*\* – dashboards on top of PostgreSQL



The goal: show how you can go from \*\*raw streaming events → ML scores → live monitoring\*\*.



---



\## Architecture



&nbsp;              ┌────────────────────┐

&nbsp;              │  Transaction        │

&nbsp;              │    Producer         │

&nbsp;              │ (Python + Faker)    │

&nbsp;              └─────────┬──────────┘

&nbsp;                        │ JSON events

&nbsp;                        ▼

&nbsp;┌───────────────────────────────────────────────────────────┐

&nbsp;│                         Kafka                             │

&nbsp;│                   Topic: transactions\_raw                 │

&nbsp;└───────────────────────┬───────────────────────────────────┘

&nbsp;                        ▼

&nbsp;            ┌──────────────────────────┐

&nbsp;            │    PySpark Streaming     │

&nbsp;            │  - Deserialize JSON      │

&nbsp;            │  - Build ML Features     │

&nbsp;            │  - Apply IsolationForest │

&nbsp;            │  - Score transactions    │

&nbsp;            └──────────┬───────────────┘

&nbsp;                       │ writes via JDBC

&nbsp;                       ▼

&nbsp;        ┌──────────────────────────────────┐

&nbsp;        │            PostgreSQL            │

&nbsp;        │ tables:                          │

&nbsp;        │  - transactions\_scored           │

&nbsp;        │  - anomalies                     │

&nbsp;        └──────────────────┬───────────────┘

&nbsp;                           ▼

&nbsp;             ┌───────────────────────────┐

&nbsp;             │          Grafana          │

&nbsp;             │ Real-time dashboards       │

&nbsp;             └───────────────────────────┘



\## Project Structure Repository layout



realtime-anomaly-detection/

│

├── streaming/

│   └── stream\_processor.py         # PySpark streaming job

│

├── producer/

│   └── transaction\_producer.py     # Kafka data generator

│

├── ml/

│   ├── prepare\_data.py             # convert JSONL → Parquet

│   ├── features.py                 # feature engineering

│   └── train\_model.py              # train Isolation Forest

│

├── models/

│   └── isolation\_forest.pkl        # saved ML model

│

├── data/

│   ├── transactions\_log.jsonl      # raw training data

│   ├── transactions.parquet

│   └── checkpoints/                # Spark checkpoints

│

├── docker-compose.yml              # Kafka + Zookeeper + PostgreSQL

├── requirements.txt

├── .gitignore

├── LICENSE

└── README.md



🛠️ Installation \& Setup

1️⃣ Clone the repo

git clone https://github.com/YOUR\_USERNAME/realtime-anomaly-detection.git

cd realtime-anomaly-detection



2️⃣ Create virtual environment

python -m venv venv

source venv/bin/activate       # Linux/Mac

venv\\Scripts\\activate          # Windows



3️⃣ Install dependencies

pip install -r requirements.txt



4️⃣ Start Kafka + Zookeeper + PostgreSQL

docker-compose up -d



📈 5️⃣ Generate Training Data



Run:



python producer/transaction\_producer.py





This generates:



Realistic transactions



5% anomalies



Saves to data/transactions\_log.jsonl



Stop when you have enough data.



🧠 6️⃣ Convert JSON → Parquet

python ml/prepare\_data.py



🤖 7️⃣ Train Isolation Forest Model

python ml/train\_model.py





Outputs:



Model saved to models/isolation\_forest.pkl



🔥 8️⃣ Start Streaming Job

python streaming/stream\_processor.py





This will:



Read Kafka events



Build features



Score anomaly score



Insert results into PostgreSQL



📊 9️⃣ Grafana Dashboards



Open browser → http://localhost:3000



Login:



user: admin



password: admin



Add PostgreSQL datasource



Build dashboards using queries:



Example: Count anomalies

SELECT

&nbsp; timestamp AS time,

&nbsp; is\_anomaly

FROM anomalies

ORDER BY time;




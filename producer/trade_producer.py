from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
USER_IDS = [101, 102, 103]

def generate_trade():
    return {
        "user_id": random.choice(USER_IDS),
        "symbol": random.choice(SYMBOLS),
        "side": random.choice(["BUY", "SELL"]),
        "price": round(random.uniform(20000, 40000), 2),
        "quantity": round(random.uniform(0.01, 0.1), 4),
        "timestamp": datetime.utcnow().isoformat()
    }

while True:
    trade = generate_trade()
    producer.send('trades', trade)
    print(f"Produced: {trade}")
    time.sleep(1)

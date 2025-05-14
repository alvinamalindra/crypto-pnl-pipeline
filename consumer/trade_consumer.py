from kafka import KafkaConsumer
import json
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="crypto_pnl",
    user="user",
    password="password"
)
cursor = conn.cursor()

# Kafka setup
consumer = KafkaConsumer(
    'trades',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='pnl-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Storing trade data...\n")

for message in consumer:
    trade = message.value
    print(f"Inserting Trade: {trade}")
    
    cursor.execute("""
        INSERT INTO trades (user_id, symbol, side, price, quantity, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        trade['user_id'],
        trade['symbol'],
        trade['side'],
        trade['price'],
        trade['quantity'],
        trade['timestamp']
    ))

    conn.commit()
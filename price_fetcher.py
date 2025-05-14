import requests
import psycopg2
from datetime import datetime

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="crypto_pnl",
    user="user",
    password="password"
)
cursor = conn.cursor()

# Symbols to fetch
symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]

def fetch_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        return float(resp.json()["price"])
    except:
        print(f"Failed to fetch {symbol}")
        return None
    
def fetch_usd_to_idr():
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        idr = data["rates"].get("IDR")
        if idr:
            return float(idr)
        else:
            print("IDR not found in response:", data)
    except Exception as e:
        print(f"Error fetching USDIDR: {e}")
    return None


for symbol in symbols:
    price = fetch_price(symbol)
    if price:
        print(f"{symbol} = {price}")
        cursor.execute("""
            INSERT INTO prices (symbol, price, timestamp)
            VALUES (%s, %s, %s)
        """, (symbol, price, datetime.utcnow()))

usd_idr = fetch_usd_to_idr()
if usd_idr:
    print(f"USDIDR = {usd_idr}")
    cursor.execute("""
        INSERT INTO prices (symbol, price, timestamp)
        VALUES (%s, %s, %s)
    """, ("USDIDR", usd_idr, datetime.utcnow()))

conn.commit()
conn.close()

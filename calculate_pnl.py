import psycopg2
from collections import defaultdict

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="crypto_pnl",
    user="user",
    password="password"
)
cursor = conn.cursor()

# Get latest prices
cursor.execute("""
    SELECT DISTINCT ON (symbol) symbol, price
    FROM prices
    ORDER BY symbol, timestamp DESC
""")
price_map = {row[0]: float(row[1]) for row in cursor.fetchall()}

# Get all trades
cursor.execute("SELECT user_id, symbol, side, price, quantity FROM trades ORDER BY timestamp")
trades = cursor.fetchall()

# PnL Calculation
positions = defaultdict(lambda: {'qty': 0, 'total_cost': 0, 'realized_pnl': 0})

for user_id, symbol, side, price, quantity in trades:
    key = (user_id, symbol)
    p = positions[key]

    if side == 'BUY':
        # Add to position
        p['qty'] += quantity
        p['total_cost'] += quantity * price

    elif side == 'SELL':
        # Realized profit = (Sell - Avg Buy) * qty sold
        if p['qty'] == 0:
            continue  # no holdings

        avg_buy = p['total_cost'] / p['qty']
        sell_pnl = (price - avg_buy) * quantity

        p['qty'] -= quantity
        p['total_cost'] -= avg_buy * quantity
        p['realized_pnl'] += sell_pnl

# Store PnL to new table
cursor.execute("DROP TABLE IF EXISTS pnl")
cursor.execute("""
    CREATE TABLE pnl (
        user_id INTEGER,
        symbol VARCHAR(20),
        avg_entry_price NUMERIC,
        total_qty NUMERIC,
        realized_pnl NUMERIC,
        unrealized_pnl NUMERIC,
        unrealized_pnl_idr NUMERIC
    )
""")

usd_idr = price_map.get('USDIDR', 0)

for (user_id, symbol), p in positions.items():
    if p['qty'] == 0:
        unrealized_pnl = 0
        avg_entry = 0
    else:
        avg_entry = float(p['total_cost']) / float(p['qty'])
        current_price = float(price_map.get(symbol, 0))
        qty = float(p['qty'])
        unrealized_pnl = (current_price - avg_entry) * qty


    unrealized_pnl_idr = unrealized_pnl * usd_idr if usd_idr else None

    cursor.execute("""
        INSERT INTO pnl (user_id, symbol, avg_entry_price, total_qty, realized_pnl, unrealized_pnl, unrealized_pnl_idr)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        symbol,
        round(avg_entry, 2),
        round(p['qty'], 4),
        round(p['realized_pnl'], 2),
        round(unrealized_pnl, 2),
        round(unrealized_pnl_idr, 2) if unrealized_pnl_idr is not None else None
    ))

conn.commit()
conn.close()
print(" PnL Calculated and saved to `pnl` table.")

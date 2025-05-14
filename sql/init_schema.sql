CREATE TABLE trades (
    trade_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    symbol VARCHAR(20),
    side VARCHAR(4),
    price NUMERIC,
    quantity NUMERIC,
    timestamp TIMESTAMPTZ
);

CREATE TABLE prices (
    symbol VARCHAR(20),
    price NUMERIC,
    timestamp TIMESTAMPTZ
);

CREATE TABLE pnl (
    user_id INTEGER,
    symbol VARCHAR(20),
    avg_entry_price NUMERIC,
    total_qty NUMERIC,
    realized_pnl NUMERIC,
    unrealized_pnl NUMERIC,
    last_updated TIMESTAMPTZ
);

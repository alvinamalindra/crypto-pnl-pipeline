# 🪙 Crypto PnL Streaming Pipeline

An end-to-end project for real-time trade tracking and PnL calculation using:

- PostgreSQL
- Redpanda (Kafka-compatible)
- Python
- Docker
- Binance API for live crypto prices
- IDR conversion via open exchange API

---

## Features

- Kafka-style producer for streaming crypto trades
- Redpanda as the streaming engine
- Real-time consumer saving trades to PostgreSQL
- External market price fetcher (BTC, ETH, BNB, USD/IDR)
- Profit & Loss calculation:
  - Realized PnL
  - Unrealized PnL
  - Conversion to IDR

---

## How to Run

1. Clone this repo
2. Start services:
   ```bash
   docker-compose up -d
   ```
3. Run the trade producer:
   ```bash
   python producer/trade_producer.py
   ```
4. Run the trade consumer:
   ```bash
   python consumer/trade_consumer.py
   ```
5. Fetch market prices:
   ```bash
   python price_fetcher.py
   ```
6. Calculate PnL:
   ```bash
   python calculate_pnl.py
   ```

---

## Example Output (`pnl` table)

| user_id | symbol   | avg_entry_price | qty    | realized_pnl | unrealized_pnl | unrealized_pnl_idr |
|---------|----------|------------------|--------|---------------|-----------------|---------------------|
| 101     | BTCUSDT  | 30000.00         | 0.02   | 120.00        | 80.00           | 1,280,000           |

---

## Future Ideas

- Build a dashboard with Streamlit or Grafana
- Use Spark for scalable batch PnL
- Store logs to ClickHouse for analytics

---

## License

MIT

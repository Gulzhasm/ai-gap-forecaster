# AI Gap Trader

A stock gap trading assistant built with Flask that scans for market gaps, manages a watchlist, logs trades, and tracks performance — part of my AI Engineer roadmap.

## What It Does

- **Gap Scanner** — Scans US stocks for gap-up/gap-down openings using Yahoo Finance data, filterable by direction and minimum gap %
- **Watchlist** — Track symbols you're watching with notes, target prices, and sector tags
- **Trade Journal** — Log entries/exits with gap type, direction, stop-loss, take-profit, and setup ratings (1-5)
- **Performance Dashboard** — Win rate, total P&L, average return, and trade history stats
- **Catalyst Tracking** — Links trades to news catalysts with sentiment scores via Finnhub
- **Interactive Brokers Integration** — Paper/live order management through IB Gateway (via `ib_insync`)
- **Risk Management** — Configurable position sizing, max daily loss, and open position limits

## Tech Stack

- **Backend:** Python / Flask / SQLAlchemy
- **Database:** SQLite
- **Market Data:** yfinance, Finnhub API
- **Broker:** Interactive Brokers (`ib_insync`)
- **Scheduler:** APScheduler
- **Frontend:** Jinja2 templates

## Project Structure

```
gap-trader/
├── app.py              # Flask app factory
├── config.py           # Environment-based configuration
├── models.py           # SQLAlchemy models (Watchlist, Trade, Catalyst, Order, RiskConfig)
├── seed.py             # Database seeding
├── routes/
│   ├── views.py        # Page routes (dashboard, watchlist, journal, performance)
│   ├── api_scanner.py  # GET /api/scanner — gap scan endpoint
│   ├── api_watchlist.py# CRUD /api/watchlist
│   ├── api_trades.py   # CRUD /api/trades
│   └── api_stats.py    # GET /api/stats — performance metrics
├── services/
│   ├── gap_scanner.py  # Core gap detection logic
│   ├── trade_service.py# Trade management
│   ├── stats_service.py# Performance calculations
│   └── symbols.py      # Default symbol list
├── templates/          # Jinja2 HTML templates
└── static/             # CSS / JS assets
```

## Getting Started

```bash
# Clone
git clone https://github.com/Gulzhasm/ai-gap-trader.git
cd ai-gap-trader

# Install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set up environment
cp .env.example .env  # Add your FINNHUB_API_KEY

# Run
python app.py
```

The app runs at `http://localhost:5001`.

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `FINNHUB_API_KEY` | Finnhub API key for catalyst data | — |
| `IB_HOST` | Interactive Brokers gateway host | `127.0.0.1` |
| `IB_PORT` | IB Gateway port (7497=TWS paper, 4002=Gateway paper) | `7497` |
| `IB_TRADING_MODE` | `paper` or `live` | `paper` |
| `RISK_MAX_POSITION_PCT` | Max position size as % of portfolio | `5.0` |
| `RISK_MAX_DAILY_LOSS` | Max daily loss limit ($) | `500.0` |

## Roadmap

- [ ] AI-powered gap fill probability prediction
- [ ] Automated trade execution via IB
- [ ] Real-time WebSocket price streaming
- [ ] Backtesting engine for gap strategies
- [ ] Multi-timeframe analysis

## License

MIT

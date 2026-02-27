# ai-gap-forecaster: RL Forecasting Engine & Adversarial UI Testbed

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Playwright](https://img.shields.io/badge/Playwright-Automated_Testing-green.svg)](https://playwright.dev/)

## Abstract

`ai-gap-forecaster` is an experimental trading application driven by Reinforcement Learning (RL) for time-series forecasting. Beyond its financial application, this repository serves a crucial meta-engineering purpose: it is an intentionally volatile frontend environment designed to stress-test AI-driven software quality systems.

By programmatically mutating DOM elements and UI locators, `ai-gap-forecaster` provides a rigorous testing ground to validate the self-healing capabilities of [ai-test-gen](https://github.com/Gulzhasm/ai-test-gen), ensuring LLM-orchestrated test automation can survive real-world application degradation.

## Overview: A Symbiotic ML Architecture

`ai-gap-forecaster` is a dual-purpose engineering project that bridges financial domain expertise with advanced machine learning quality systems. On the surface, it is a time-series forecasting application utilizing Reinforcement Learning (RL) agents to navigate market gaps.

Beneath the surface, it is an **Adversarial UI Testbed**. The frontend architecture is deliberately engineered to mutate -- simulating the unpredictable UI changes found in agile enterprise environments. This controlled volatility creates the perfect ground-truth environment to train, test, and validate the self-healing Playwright locators of the primary research project, [ai-test-gen](https://github.com/Gulzhasm/ai-test-gen).

## Core Objectives

- **Time-Series Forecasting:** Implement RL algorithms (e.g., Proximal Policy Optimization) to identify and act upon price gaps in financial time-series data.
- **Adversarial DOM Mutation:** Programmatic shifting of UI locators, component hierarchies, and CSS classes to simulate frontend degradation.
- **ML Pipeline Validation:** Provide a closed-loop ecosystem to measure the recovery rate, latency, and accuracy of the ai-test-gen LLM+RAG self-healing mechanism.

## System Architecture

The system operates as a closed loop between two distinct machine learning pipelines:

**The Target (The RL Agent):** A Python-based backend feeding real-time financial data to a dynamic frontend dashboard.

**The Observer (The LLM Test Agent):** The ai-test-gen framework, which continuously monitors the dashboard, detects structural DOM mutations, and dynamically repairs broken Playwright locators via semantic matching (ChromaDB) and LLM reasoning.

### Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python, Flask 3.1, SQLAlchemy |
| **Machine Learning** | PyTorch, Reinforcement Learning (PPO/DQN), Time-Series Analysis |
| **Market Data** | yfinance, Finnhub API |
| **Broker Integration** | Interactive Brokers (`ib_insync`) |
| **Database** | SQLite (dev), PostgreSQL (prod) |
| **Frontend/UI** | Jinja2 templates, Bootstrap 5, Chart.js, Dynamic DOM generation |
| **Quality Assurance** | Playwright, LLM-based Self-Healing Locators ([ai-test-gen](https://github.com/Gulzhasm/ai-test-gen)) |

## Why This Exists (The Meta-Project)

Modern web applications undergo constant iteration, causing deterministic UI tests to fail. `ai-gap-forecaster` acts as an "Adversarial UI." By controlling the exact rate and nature of frontend mutations, we can mathematically quantify the success rate, semantic accuracy, and latency of automated test-healing pipelines.

## Current Capabilities

- **Gap Scanner** -- Scans 60+ US stocks for gap-up/gap-down openings using Yahoo Finance data
- **Watchlist** -- Track symbols with notes, target prices, and sector tags
- **Trade Journal** -- Log entries/exits with gap type, direction, and setup ratings
- **Performance Dashboard** -- Win rate, total P&L, cumulative charts, and gap-type breakdowns
- **Catalyst Tracking** -- Links trades to news catalysts with sentiment scores via Finnhub
- **IB Integration** -- Paper/live order management through Interactive Brokers Gateway

## Project Structure

```
ai-gap-forecaster/
├── app.py              # Flask app factory with prefix middleware
├── wsgi.py             # Production WSGI entry point
├── config.py           # Environment-based configuration
├── models.py           # SQLAlchemy models (Watchlist, Trade, Catalyst, Order, RiskConfig)
├── seed.py             # Database seeding
├── render.yaml         # Render deployment config
├── routes/
│   ├── views.py        # Page routes (dashboard, watchlist, journal, performance)
│   ├── api_scanner.py  # GET /api/scanner -- gap scan endpoint
│   ├── api_watchlist.py# CRUD /api/watchlist
│   ├── api_trades.py   # CRUD /api/trades
│   └── api_stats.py    # GET /api/stats -- performance metrics
├── services/
│   ├── gap_scanner.py  # Core gap detection logic
│   ├── trade_service.py# Trade management & P&L calculations
│   ├── stats_service.py# Performance analytics
│   └── symbols.py      # Default symbol list (60+ large-cap stocks)
├── templates/          # Jinja2 HTML templates (mutating DOM targets)
└── static/             # CSS / JS assets
```

## Getting Started

```bash
git clone https://github.com/Gulzhasm/ai-gap-forecaster.git
cd ai-gap-forecaster

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env  # Add your FINNHUB_API_KEY

python app.py
```

The app runs at `http://localhost:5001`.

## Deployment

Deployed at [gulzhasml.com/ai-gap-forecaster](https://gulzhasml.com/ai-gap-forecaster) via Render (Flask backend) + Vercel rewrites (Next.js portfolio proxy).

## Roadmap

- [ ] Phase 1: Data ingestion pipeline and baseline RL model implementation
- [ ] Phase 2: Development of the dynamic trading dashboard
- [ ] Phase 3: Implementation of the "Adversarial UI" mutation engine (randomized ID/class shifting)
- [ ] Phase 4: Cross-repository integration with `ai-test-gen` for live self-healing validation
- [ ] Phase 5: Automated trade execution via IB & real-time WebSocket streaming

## License

MIT

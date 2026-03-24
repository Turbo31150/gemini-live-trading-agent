<div align="center">
  <img src="assets/logo.svg" alt="GEMINI·LIVE·TRADER" width="520"/>
  <br/><br/>

  [![License: MIT](https://img.shields.io/badge/License-MIT-34D399?style=for-the-badge)](LICENSE)
  [![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
  [![Gemini](https://img.shields.io/badge/Gemini_Live_API-Google_Cloud-4285F4?style=for-the-badge&logo=google&logoColor=white)](#)
  [![Trading](https://img.shields.io/badge/Trading-Crypto-F59E0B?style=for-the-badge&logo=bitcoin&logoColor=white)](#)
  [![Real-time](https://img.shields.io/badge/Real--time-Market_Data-EF4444?style=for-the-badge&logo=lightning&logoColor=white)](#)
  [![Voice](https://img.shields.io/badge/Voice-Orders-FBBF24?style=for-the-badge&logo=google-assistant&logoColor=white)](#)
  [![JARVIS](https://img.shields.io/badge/JARVIS-Ecosystem-8B5CF6?style=for-the-badge&logo=probot&logoColor=white)](https://github.com/Turbo31150/jarvis-linux)

  <br/>

  [![Stars](https://img.shields.io/github/stars/Turbo31150/gemini-live-trading-agent?style=flat-square&color=34D399)](https://github.com/Turbo31150/gemini-live-trading-agent/stargazers)
  [![Forks](https://img.shields.io/github/forks/Turbo31150/gemini-live-trading-agent?style=flat-square&color=FBBF24)](https://github.com/Turbo31150/gemini-live-trading-agent/network/members)
  [![Issues](https://img.shields.io/github/issues/Turbo31150/gemini-live-trading-agent?style=flat-square&color=EF4444)](https://github.com/Turbo31150/gemini-live-trading-agent/issues)
  [![Last Commit](https://img.shields.io/github/last-commit/Turbo31150/gemini-live-trading-agent?style=flat-square&color=4285F4)](https://github.com/Turbo31150/gemini-live-trading-agent/commits)

  <br/>
  <h3>Real-Time Voice Trading Assistant · Gemini Live API · Voice Orders · Live Markets</h3>
  <p><em>Execute trading orders by voice — Gemini analyzes markets in real-time and runs your strategies</em></p>
</div>

---

## Overview

**GEMINI·LIVE·TRADER** is a voice-first trading assistant built on the **Gemini Live API**. It lets you place orders, analyze markets, and manage positions entirely through voice commands — with real-time AI analysis powered by Gemini.

Say *"Buy 0.1 BTC at market"* and it executes. Ask *"What's the BTC RSI on 4h?"* and it answers out loud.

> **Why voice trading?** In volatile markets, speed matters. Voice commands let you react instantly without navigating complex UIs — hands-free, eyes on the chart.

---

## Trading Features

| Feature | Description | Status |
|---------|-------------|--------|
| **Voice Orders** | Natural language order placement — "Buy 0.1 BTC at market" | Active |
| **Real-Time Analysis** | Gemini analyzes price, volume, and momentum as markets move | Active |
| **Technical Q&A** | Ask RSI, MACD, Bollinger, support/resistance — get spoken answers | Active |
| **Smart Alerts** | Voice notifications on market events, stop-loss triggers, anomalies | Active |
| **Portfolio Reports** | "Show my PnL" — instant spoken portfolio summary | Active |
| **Multi-Exchange** | Pluggable execution layer — Binance, Kraken, CCXT-compatible | Active |
| **Streaming Audio** | Full-duplex voice — listen and speak simultaneously | Active |
| **Risk Management** | Position sizing, stop-loss, take-profit voice configuration | Active |

---

## Voice Commands

| Category | Command | Action |
|----------|---------|--------|
| **Orders** | *"Buy 0.5 ETH at market"* | Market buy order |
| **Orders** | *"Place a limit sell 1 BTC at $70,000"* | Limit sell order |
| **Orders** | *"Cancel all open orders"* | Batch cancel |
| **Analysis** | *"What's the RSI on BTC 4h?"* | Technical indicator query |
| **Analysis** | *"Give me a market summary"* | Multi-asset overview |
| **Portfolio** | *"Show my open positions"* | Position list with PnL |
| **Portfolio** | *"What's my total PnL today?"* | Daily performance |
| **Alerts** | *"Alert me if ETH drops below $3,500"* | Price alert |
| **Risk** | *"Set stop-loss at -5% on all positions"* | Risk management |

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     User (Microphone)                     │
│              "Buy 0.1 BTC at market"                      │
└──────────────────────┬───────────────────────────────────┘
                       │ voice stream
                       ▼
┌──────────────────────────────────────────────────────────┐
│             Gemini Live API (Google Cloud)                 │
│          STT  ←→  LLM Reasoning  ←→  TTS                 │
│                                                           │
│   ┌─────────────────────────────────────────────────────┐ │
│   │  Context: portfolio state, market data, risk rules  │ │
│   └─────────────────────────────────────────────────────┘ │
└──────────────────────┬───────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────┐
│                    Intent Parser                          │
│  ┌──────────────┬───────────────┬─────────────────────┐  │
│  │ MARKET_DATA  │ PLACE_ORDER   │   PORTFOLIO         │  │
│  │ fetch price  │ validate &    │   positions &       │  │
│  │ & indicators │ execute order │   PnL summary       │  │
│  └──────────────┴───────────────┴─────────────────────┘  │
│  ┌──────────────┬───────────────┬─────────────────────┐  │
│  │ ANALYSIS     │ ALERTS        │   RISK              │  │
│  │ TA + AI      │ price/volume  │   stop-loss, sizing │  │
│  │ summary      │ triggers      │   management        │  │
│  └──────────────┴───────────────┴─────────────────────┘  │
└──────────────────────┬───────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────┐
│              Execution Layer (Exchange API)                │
│            Binance · Kraken · CCXT-compatible              │
│                                                           │
│   Order validation → Rate limiting → Execution → Confirm  │
└──────────────────────┬───────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────┐
│           Voice Response (Gemini TTS streaming)           │
│        "Order confirmed: 0.1 BTC bought at $67,432"       │
└──────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- Google Cloud account with Gemini API access
- Exchange API key (Binance, Kraken, or CCXT-compatible)
- Microphone for voice commands

### Installation

```bash
# Clone the repository
git clone https://github.com/Turbo31150/gemini-live-trading-agent.git
cd gemini-live-trading-agent

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Google Cloud credentials
export GOOGLE_API_KEY=AIza...

# Exchange API (example: Binance)
export EXCHANGE_API_KEY=your_exchange_key
export EXCHANGE_SECRET=your_exchange_secret

# Optional: specify exchange (default: binance)
export EXCHANGE_NAME=binance
```

### Run

```bash
python main.py
```

> The assistant starts listening immediately. Speak your first command to begin trading.

---

## Usage Examples

```
You:    "What's the current price of ETH?"
Gemini: "Ethereum is trading at $3,842, up 2.3% in the last 24 hours.
         Volume is 18.2B — above average."

You:    "Place a limit buy for 1 ETH at $3,800."
Gemini: "Limit buy order placed: 1 ETH at $3,800. I'll notify you when it fills."

You:    "Show my open positions."
Gemini: "You have 2 open positions:
         • 0.5 BTC — in profit at +4.1% ($1,384)
         • 100 SOL — down at -1.2% (-$58)
         Total unrealized PnL: +$1,326."

You:    "What's the RSI on BTC daily?"
Gemini: "BTC daily RSI is at 62.4 — neutral zone, approaching overbought.
         MACD is bullish with a recent crossover."
```

---

## Supported Exchanges

| Exchange | Status | Features |
|----------|--------|----------|
| Binance | Supported | Spot, Futures, Margin |
| Kraken | Supported | Spot |
| Any CCXT | Compatible | Via CCXT unified API |

---

## JARVIS Ecosystem

This project is part of the **JARVIS** distributed AI cluster:

| Project | Description |
|---------|-------------|
| [jarvis-linux](https://github.com/Turbo31150/jarvis-linux) | Distributed Autonomous AI Cluster |
| [TradeOracle](https://github.com/Turbo31150/TradeOracle) | Autonomous Crypto Trading Agent |
| [lumen](https://github.com/Turbo31150/lumen) | Multilingual Live AI Web App |
| [gemini-creative-storyteller](https://github.com/Turbo31150/gemini-creative-storyteller) | Interactive AI Storyteller |
| [gemini-ui-navigator-agent](https://github.com/Turbo31150/gemini-ui-navigator-agent) | Voice Web Browser Agent |
| **gemini-live-trading-agent** | Voice Trading Assistant *(this repo)* |

---

## Disclaimer

This software is provided for educational and research purposes. Trading cryptocurrencies involves significant risk. Always do your own research and never trade with funds you cannot afford to lose.

---

## License

MIT © 2026 [Turbo31150](https://github.com/Turbo31150) — Franck Delmas

> Built with Google Cloud · Gemini Live API · CCXT

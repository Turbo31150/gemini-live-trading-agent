"""Configuration for Gemini Live Trading Agent."""

import os

# Google Cloud
PROJECT_ID = os.environ.get("PROJECT_ID", "")
LOCATION = os.environ.get("LOCATION", "us-central1")
MODEL = os.environ.get("MODEL", "gemini-live-2.5-flash-native-audio")

# Server
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8080"))
DEV_MODE = os.environ.get("DEV_MODE", "true").lower() == "true"
SESSION_TIME_LIMIT = int(os.environ.get("SESSION_TIME_LIMIT", "300"))  # 5 min

# Trading
TRADING_PAIRS = [
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "ADA/USDT",
    "DOGE/USDT", "AVAX/USDT", "LINK/USDT", "DOT/USDT", "MATIC/USDT",
]
DEFAULT_EXCHANGE = "binance"

# Voice
DEFAULT_VOICE = "Puck"  # Gemini voice preset
AVAILABLE_VOICES = ["Puck", "Charon", "Kore", "Fenrir", "Aoede"]

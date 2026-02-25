"""Market data tools for Gemini function calling.

These tools are registered with Gemini Live API and called
when the user asks about market data, prices, or analysis.
"""

import asyncio
import json
from datetime import datetime, timezone
from google.genai import types


# ── Tool Declarations (sent to Gemini in LiveConnectConfig) ──────────────

TOOL_DECLARATIONS = [
    types.FunctionDeclaration(
        name="get_market_price",
        description="Get the current price, 24h change, and volume for a cryptocurrency trading pair",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "symbol": types.Schema(
                    type=types.Type.STRING,
                    description="Trading pair symbol, e.g. BTC/USDT, ETH/USDT, SOL/USDT",
                ),
            },
            required=["symbol"],
        ),
    ),
    types.FunctionDeclaration(
        name="get_market_overview",
        description="Get an overview of the top cryptocurrency markets with prices and changes",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "limit": types.Schema(
                    type=types.Type.INTEGER,
                    description="Number of top markets to return, default 5",
                ),
            },
        ),
    ),
    types.FunctionDeclaration(
        name="get_technical_analysis",
        description="Get technical analysis indicators for a trading pair including RSI, MACD, moving averages",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "symbol": types.Schema(
                    type=types.Type.STRING,
                    description="Trading pair symbol, e.g. BTC/USDT",
                ),
            },
            required=["symbol"],
        ),
    ),
    types.FunctionDeclaration(
        name="get_risk_assessment",
        description="Assess the current risk level for a cryptocurrency position based on volatility, sentiment, and market conditions",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "symbol": types.Schema(
                    type=types.Type.STRING,
                    description="Trading pair symbol",
                ),
                "position_size_usd": types.Schema(
                    type=types.Type.NUMBER,
                    description="Position size in USD",
                ),
            },
            required=["symbol"],
        ),
    ),
    types.FunctionDeclaration(
        name="set_price_alert",
        description="Set a price alert that will notify the user when the price crosses a threshold",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "symbol": types.Schema(
                    type=types.Type.STRING,
                    description="Trading pair symbol",
                ),
                "target_price": types.Schema(
                    type=types.Type.NUMBER,
                    description="Target price to trigger the alert",
                ),
                "direction": types.Schema(
                    type=types.Type.STRING,
                    description="Alert direction: above or below",
                    enum=["above", "below"],
                ),
            },
            required=["symbol", "target_price", "direction"],
        ),
    ),
]


# ── Tool Implementations ────────────────────────────────────────────────

_exchange = None
_alerts: list[dict] = []


def _get_exchange():
    """Lazy-init CCXT exchange."""
    global _exchange
    if _exchange is None:
        import ccxt.async_support as ccxt
        _exchange = ccxt.binance({"enableRateLimit": True})
    return _exchange


async def get_market_price(symbol: str) -> dict:
    """Fetch current price data for a symbol."""
    try:
        exchange = _get_exchange()
        ticker = await exchange.fetch_ticker(symbol.upper())
        return {
            "symbol": symbol.upper(),
            "price": ticker.get("last", 0),
            "change_24h_pct": round(ticker.get("percentage", 0) or 0, 2),
            "high_24h": ticker.get("high", 0),
            "low_24h": ticker.get("low", 0),
            "volume_24h_usd": round(ticker.get("quoteVolume", 0) or 0, 0),
            "bid": ticker.get("bid", 0),
            "ask": ticker.get("ask", 0),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol}


async def get_market_overview(limit: int = 5) -> dict:
    """Fetch overview of top markets."""
    from src.config import TRADING_PAIRS
    exchange = _get_exchange()
    pairs = TRADING_PAIRS[:limit]

    try:
        tickers = await exchange.fetch_tickers(pairs)
        markets = []
        for symbol in pairs:
            t = tickers.get(symbol, {})
            markets.append({
                "symbol": symbol,
                "price": t.get("last", 0),
                "change_24h_pct": round(t.get("percentage", 0) or 0, 2),
                "volume_24h_usd": round(t.get("quoteVolume", 0) or 0, 0),
            })

        markets.sort(key=lambda x: abs(x["change_24h_pct"]), reverse=True)
        return {
            "markets": markets,
            "count": len(markets),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        return {"error": str(e)}


async def get_technical_analysis(symbol: str) -> dict:
    """Compute basic technical indicators from OHLCV data."""
    import numpy as np
    exchange = _get_exchange()

    try:
        ohlcv = await exchange.fetch_ohlcv(symbol.upper(), "1h", limit=50)
        closes = np.array([c[4] for c in ohlcv])

        # RSI (14 periods)
        deltas = np.diff(closes)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        avg_gain = np.mean(gains[-14:])
        avg_loss = np.mean(losses[-14:])
        rs = avg_gain / max(avg_loss, 1e-10)
        rsi = 100 - (100 / (1 + rs))

        # Moving averages
        sma_20 = float(np.mean(closes[-20:]))
        sma_50 = float(np.mean(closes[-50:])) if len(closes) >= 50 else sma_20
        ema_12 = float(closes[-1])  # Simplified
        ema_26 = float(np.mean(closes[-26:])) if len(closes) >= 26 else ema_12

        # MACD
        macd = ema_12 - ema_26

        # Volatility
        returns = np.diff(closes) / closes[:-1]
        volatility = float(np.std(returns) * np.sqrt(24)) * 100  # Annualized daily

        price = float(closes[-1])
        trend = "bullish" if price > sma_20 > sma_50 else "bearish" if price < sma_20 < sma_50 else "neutral"

        return {
            "symbol": symbol.upper(),
            "price": price,
            "rsi_14": round(float(rsi), 1),
            "sma_20": round(sma_20, 2),
            "sma_50": round(sma_50, 2),
            "macd": round(float(macd), 4),
            "volatility_pct": round(volatility, 2),
            "trend": trend,
            "signal": "overbought" if rsi > 70 else "oversold" if rsi < 30 else "neutral",
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol}


async def get_risk_assessment(symbol: str, position_size_usd: float = 1000) -> dict:
    """Assess risk for a position."""
    ta = await get_technical_analysis(symbol)
    if "error" in ta:
        return ta

    price_data = await get_market_price(symbol)
    vol = ta.get("volatility_pct", 0)
    rsi = ta.get("rsi_14", 50)
    change = price_data.get("change_24h_pct", 0)

    # Risk score 0-100
    risk_score = 0
    risk_score += min(vol * 2, 40)  # Volatility contribution (max 40)
    risk_score += abs(change) * 2   # 24h change contribution
    if rsi > 75 or rsi < 25:
        risk_score += 20  # Extreme RSI
    risk_score = min(int(risk_score), 100)

    var_95 = position_size_usd * (vol / 100) * 1.645
    level = "LOW" if risk_score < 30 else "MEDIUM" if risk_score < 60 else "HIGH" if risk_score < 80 else "CRITICAL"

    return {
        "symbol": symbol.upper(),
        "risk_score": risk_score,
        "risk_level": level,
        "volatility_pct": vol,
        "rsi": rsi,
        "change_24h_pct": change,
        "position_size_usd": position_size_usd,
        "value_at_risk_95": round(var_95, 2),
        "recommendation": (
            "Consider reducing position" if risk_score > 70
            else "Monitor closely" if risk_score > 40
            else "Position looks safe"
        ),
    }


async def set_price_alert(symbol: str, target_price: float, direction: str) -> dict:
    """Set a price alert."""
    alert = {
        "id": len(_alerts) + 1,
        "symbol": symbol.upper(),
        "target_price": target_price,
        "direction": direction,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "active",
    }
    _alerts.append(alert)
    return {
        "message": f"Alert set for {symbol.upper()} {direction} {target_price}",
        "alert": alert,
    }


# ── Tool Dispatcher ─────────────────────────────────────────────────────

TOOL_HANDLERS = {
    "get_market_price": get_market_price,
    "get_market_overview": get_market_overview,
    "get_technical_analysis": get_technical_analysis,
    "get_risk_assessment": get_risk_assessment,
    "set_price_alert": set_price_alert,
}


async def execute_tool(name: str, args: dict) -> str:
    """Execute a tool by name and return JSON result."""
    handler = TOOL_HANDLERS.get(name)
    if not handler:
        return json.dumps({"error": f"Unknown tool: {name}"})
    result = await handler(**args)
    return json.dumps(result, default=str)

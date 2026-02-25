"""Gemini Live Trading Agent — FastAPI backend.

WebSocket endpoint proxies audio between browser and Gemini Live API.
Serves the frontend static files.
"""

import asyncio
import json
import logging
import os
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.config import HOST, PORT, SESSION_TIME_LIMIT, DEV_MODE
from src.agents.live_trader import LiveTradingSession

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Gemini Live Trading Agent")

# ── WebSocket endpoint ──────────────────────────────────────────────────


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle a single live trading session over WebSocket."""
    await websocket.accept()
    logger.info("Client connected")

    session = LiveTradingSession()

    async def audio_output_callback(data: bytes):
        """Send audio from Gemini to the browser."""
        try:
            await websocket.send_bytes(data)
        except Exception:
            session.stop()

    async def handle_client_messages():
        """Read messages from the browser and feed to Gemini."""
        try:
            while True:
                message = await websocket.receive()
                if "bytes" in message:
                    # Binary = PCM audio from microphone
                    await session.feed_audio(message["bytes"])
                elif "text" in message:
                    # JSON = control messages
                    data = json.loads(message["text"])
                    if data.get("type") == "stop":
                        session.stop()
                        break
        except WebSocketDisconnect:
            session.stop()
        except Exception as e:
            logger.error(f"Client message error: {e}")
            session.stop()

    async def run_session():
        """Run the Gemini Live session and forward events to client."""
        client_task = asyncio.create_task(handle_client_messages())

        try:
            async for event in session.start(audio_output_callback):
                try:
                    await websocket.send_json(event)
                except Exception:
                    break
        finally:
            client_task.cancel()
            try:
                await client_task
            except asyncio.CancelledError:
                pass

    try:
        await asyncio.wait_for(run_session(), timeout=SESSION_TIME_LIMIT)
    except asyncio.TimeoutError:
        logger.info("Session time limit reached")
        try:
            await websocket.send_json({
                "type": "session_ended",
                "reason": "time_limit",
            })
        except Exception:
            pass
    except Exception as e:
        logger.error(f"Session error: {e}")
    finally:
        try:
            await websocket.close(code=1000, reason="Session ended")
        except Exception:
            pass
        logger.info("Client disconnected")


# ── Health check ────────────────────────────────────────────────────────


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "gemini-live-trading-agent"}


# ── Static frontend ─────────────────────────────────────────────────────

STATIC_DIR = Path(__file__).parent.parent / "public" / "dist"
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
else:
    # Dev mode: serve from public/ directly
    PUBLIC_DIR = Path(__file__).parent.parent / "public"
    if PUBLIC_DIR.exists():
        @app.get("/")
        async def index():
            return FileResponse(str(PUBLIC_DIR / "index.html"))

        app.mount("/", StaticFiles(directory=str(PUBLIC_DIR)), name="public")


# ── Entry point ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting Gemini Live Trading Agent on {HOST}:{PORT}")
    logger.info(f"Dev mode: {DEV_MODE}")
    uvicorn.run(
        "src.main:app",
        host=HOST,
        port=PORT,
        reload=DEV_MODE,
        ws_max_size=16 * 1024 * 1024,
    )

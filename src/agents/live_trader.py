"""Gemini Live Trading Agent — real-time voice interaction.

Manages a bidirectional audio session with Gemini Live API.
Pattern: Browser <-> WebSocket <-> FastAPI <-> Gemini Live API
"""

import asyncio
import json
import logging
from google import genai
from google.genai import types

from src.config import PROJECT_ID, LOCATION, MODEL, DEFAULT_VOICE, SESSION_TIME_LIMIT
from src.tools.market_tools import TOOL_DECLARATIONS, execute_tool

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are Sentinel, an elite real-time trading assistant powered by AI.
You speak naturally, concisely, and with confidence like a professional Wall Street trader.

Your capabilities:
- Fetch live cryptocurrency prices and market data
- Perform technical analysis (RSI, MACD, moving averages, volatility)
- Assess portfolio risk (VaR, risk scores, recommendations)
- Set price alerts for the user
- Give market overviews with top movers

Behavior guidelines:
- Be direct and data-driven, give numbers first then brief analysis
- When the user asks about a coin, always fetch the latest data using your tools
- Proactively mention if you see extreme RSI, high volatility, or unusual moves
- Use trader jargon naturally (support, resistance, breakout, pullback)
- Keep responses concise for voice, max 2-3 sentences unless asked for detail
- If the user interrupts you, stop immediately and listen
- You can be slightly casual but always professional
- When greeting, introduce yourself briefly as Sentinel

Example interactions:
User: "How's Bitcoin doing?"
You: [call get_market_price for BTC/USDT, then respond with price and key data]

User: "Give me the full picture on Ethereum"
You: [call get_market_price AND get_technical_analysis for ETH/USDT, then give comprehensive analysis]

User: "What are the top movers?"
You: [call get_market_overview, then report the biggest movers]
"""


class LiveTradingSession:
    """Manages a single Gemini Live audio session."""

    def __init__(self):
        self.client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location=LOCATION,
        )
        self.audio_input_queue: asyncio.Queue[bytes] = asyncio.Queue()
        self.event_queue: asyncio.Queue[dict | None] = asyncio.Queue()
        self._running = False

    def _build_config(self, voice: str = DEFAULT_VOICE) -> types.LiveConnectConfig:
        """Build the Gemini Live session configuration."""
        return types.LiveConnectConfig(
            response_modalities=[types.Modality.AUDIO],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=voice,
                    )
                )
            ),
            system_instruction=types.Content(
                parts=[types.Part(text=SYSTEM_PROMPT)]
            ),
            proactivity=types.ProactivityConfig(proactive_audio=True),
            tools=[types.Tool(function_declarations=TOOL_DECLARATIONS)],
            input_audio_transcription=types.AudioTranscriptionConfig(),
            output_audio_transcription=types.AudioTranscriptionConfig(),
        )

    async def _send_audio(self, session):
        """Continuously send audio chunks from queue to Gemini."""
        while self._running:
            try:
                chunk = await asyncio.wait_for(
                    self.audio_input_queue.get(), timeout=1.0
                )
                await session.send_realtime_input(
                    audio=types.Blob(
                        data=chunk,
                        mime_type="audio/pcm;rate=16000",
                    )
                )
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Send audio error: {e}")
                break

    async def _receive_loop(self, session, audio_callback):
        """Receive responses from Gemini and dispatch events."""
        try:
            async for response in session.receive():
                if not self._running:
                    break

                server_content = response.server_content
                tool_call = response.tool_call

                if server_content:
                    # Audio output from model
                    if server_content.model_turn:
                        for part in server_content.model_turn.parts:
                            if part.inline_data:
                                await audio_callback(part.inline_data.data)

                    # Input transcription (user speech to text)
                    if server_content.input_transcription:
                        text = server_content.input_transcription.text
                        if text and text.strip():
                            await self.event_queue.put({
                                "type": "input_transcription",
                                "text": text.strip(),
                            })

                    # Output transcription (model speech to text)
                    if server_content.output_transcription:
                        text = server_content.output_transcription.text
                        if text and text.strip():
                            await self.event_queue.put({
                                "type": "output_transcription",
                                "text": text.strip(),
                            })

                    # Turn complete
                    if server_content.turn_complete:
                        await self.event_queue.put({"type": "turn_complete"})

                    # Interrupted by user
                    if server_content.interrupted:
                        await self.event_queue.put({"type": "interrupted"})

                # Tool/function calls from Gemini
                if tool_call:
                    for fc in tool_call.function_calls:
                        logger.info(f"Tool call: {fc.name}({fc.args})")
                        await self.event_queue.put({
                            "type": "tool_call",
                            "name": fc.name,
                            "args": dict(fc.args) if fc.args else {},
                        })

                        # Execute the tool
                        result = await execute_tool(
                            fc.name,
                            dict(fc.args) if fc.args else {},
                        )

                        await self.event_queue.put({
                            "type": "tool_result",
                            "name": fc.name,
                            "result": json.loads(result),
                        })

                        # Send result back to Gemini
                        await session.send_tool_response(
                            function_responses=[
                                types.FunctionResponse(
                                    name=fc.name,
                                    response={"result": result},
                                )
                            ]
                        )

        except Exception as e:
            logger.error(f"Receive loop error: {e}")
        finally:
            await self.event_queue.put(None)  # Sentinel: session ended

    async def start(self, audio_callback):
        """Start the live session. Yields events from the event queue.

        Args:
            audio_callback: async callable that receives PCM audio bytes to send to client
        """
        self._running = True
        config = self._build_config()

        logger.info(f"Connecting to Gemini Live: model={MODEL}")

        async with self.client.aio.live.connect(model=MODEL, config=config) as session:
            send_task = asyncio.create_task(self._send_audio(session))
            recv_task = asyncio.create_task(
                self._receive_loop(session, audio_callback)
            )

            try:
                while self._running:
                    try:
                        event = await asyncio.wait_for(
                            self.event_queue.get(), timeout=5.0
                        )
                    except asyncio.TimeoutError:
                        continue
                    if event is None:
                        break
                    yield event
            except asyncio.CancelledError:
                pass
            finally:
                self._running = False
                send_task.cancel()
                recv_task.cancel()
                try:
                    await send_task
                except asyncio.CancelledError:
                    pass
                try:
                    await recv_task
                except asyncio.CancelledError:
                    pass

    def stop(self):
        """Stop the session."""
        self._running = False

    async def feed_audio(self, data: bytes):
        """Feed audio data from client microphone."""
        await self.audio_input_queue.put(data)

# Architecture Diagram

## System Overview

```
+--------------------------------------------------+
|                   USER (Browser)                  |
|                                                   |
|  +------------+  +----------+  +---------------+  |
|  | Microphone |  | Speaker  |  |  Transcript   |  |
|  | (16kHz PCM)|  | (24kHz)  |  |    Panel      |  |
|  +-----+------+  +----^-----+  +-------^-------+  |
|        |              |                |           |
|        v              |                |           |
|  +-----+--------------+----------------+--------+  |
|  |          WebSocket (wss://)                   |  |
|  |    Binary frames = PCM audio                  |  |
|  |    Text frames   = JSON events                |  |
|  +-----+------------------^---------------------+  |
+---------|-----------------|-----------------------+
          |                 |
          v                 |
+---------+-----------------+-----------------------+
|              Google Cloud Run                      |
|                                                    |
|  +----------------------------------------------+ |
|  |          FastAPI Server (Python)              | |
|  |                                               | |
|  |  /ws          WebSocket endpoint              | |
|  |  /api/health  Health check                    | |
|  |  /            Static frontend (index.html)    | |
|  +------+-------------------^--------------------+ |
|         |                   |                      |
|         v                   |                      |
|  +------+-------------------+--------------------+ |
|  |        LiveTradingSession                     | |
|  |                                               | |
|  |  audio_input_queue --> send_realtime_input()  | |
|  |  receive() --> audio_callback + events        | |
|  |                                               | |
|  |  Tool execution:                              | |
|  |    get_market_price()                         | |
|  |    get_technical_analysis()                   | |
|  |    get_risk_assessment()                      | |
|  |    get_market_overview()                      | |
|  |    set_price_alert()                          | |
|  +------+-------------------^--------------------+ |
|         |                   |                      |
+---------+-------------------+----------------------+
          |                   |
          v                   |
+---------+-------------------+----------------------+
|           Gemini Live API (Vertex AI)              |
|                                                    |
|  Model: gemini-live-2.5-flash-native-audio         |
|                                                    |
|  Features:                                         |
|    - Bidirectional audio streaming                 |
|    - Function calling (tools)                      |
|    - Input/Output transcription                    |
|    - Voice interruption handling                   |
|    - Proactive audio responses                     |
|                                                    |
+----------------------------------------------------+
          |
          v
+---------+------------------------------------------+
|              External Data (CCXT)                  |
|                                                    |
|  Binance API:                                      |
|    - Real-time ticker prices                       |
|    - OHLCV candlestick data                        |
|    - 24h volume and change                         |
|    - Order book data                               |
|                                                    |
+----------------------------------------------------+
```

## Data Flow

```
1. User speaks into microphone
   Browser captures at 16kHz, converts Float32 -> Int16 PCM
   Sends as binary WebSocket frame

2. FastAPI receives PCM bytes
   Queues in audio_input_queue
   Forwards to Gemini via send_realtime_input()

3. Gemini processes speech
   Recognizes intent, calls tools if needed
   Generates voice response

4. Tool execution (when Gemini calls a function):
   Gemini sends FunctionCall -> FastAPI executes -> returns FunctionResponse
   Gemini incorporates result into voice response

5. Audio response flows back
   Gemini streams PCM audio chunks (24kHz)
   FastAPI forwards as binary WebSocket frames
   Browser decodes and plays through speaker

6. Transcriptions sent as JSON events
   Input transcription  -> displayed as user message
   Output transcription -> displayed as agent message
   Tool calls/results   -> displayed as tool messages
```

## Google Cloud Services Used

| Service | Purpose |
|---------|---------|
| **Cloud Run** | Hosts the FastAPI server (WebSocket + static frontend) |
| **Vertex AI** | Gemini Live API for real-time voice interaction |
| **Cloud Build** | Builds Docker container image for deployment |
| **Container Registry** | Stores the built container image |

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Vanilla HTML/JS, WebSocket, Web Audio API |
| Backend | Python, FastAPI, uvicorn |
| AI Model | Gemini 2.5 Flash (Native Audio) via Vertex AI |
| SDK | Google GenAI SDK (`google-genai`) |
| Market Data | CCXT (Binance async) |
| Hosting | Google Cloud Run |
| Container | Docker (Python 3.12 slim) |

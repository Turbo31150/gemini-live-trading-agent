# Sentinel — Live Trading Agent

Real-time voice-powered cryptocurrency trading assistant built with **Gemini Live API** on **Google Cloud**.

Speak naturally to get live prices, technical analysis, risk assessments, and market overviews — all through voice interaction.

## Architecture

```
Browser (Mic/Speaker) <--WebSocket--> Cloud Run (FastAPI) <--Live API--> Gemini 2.5 Flash
                                           |
                                      CCXT/Binance
                                    (Market Data)
```

See [docs/architecture.md](docs/architecture.md) for the full architecture diagram.

## Features

- **Voice-first**: Speak naturally, get spoken responses with data
- **Live market data**: Real-time prices from Binance via CCXT
- **Technical analysis**: RSI, MACD, SMA, volatility indicators
- **Risk assessment**: VaR calculation, risk scoring, position recommendations
- **Price alerts**: Set voice-triggered price alerts
- **Market overview**: Top movers and market summary
- **Interruption handling**: Cut the agent off mid-sentence, it stops immediately

## Google Cloud Services

| Service | Usage |
|---------|-------|
| **Vertex AI** | Gemini Live API — bidirectional audio streaming with function calling |
| **Cloud Run** | Hosts the FastAPI WebSocket server and static frontend |
| **Cloud Build** | Builds the Docker container image |
| **Container Registry** | Stores the container image |

## Prerequisites

- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) (`gcloud`)
- [Python 3.11+](https://www.python.org/downloads/)
- A Google Cloud project with billing enabled
- Vertex AI API enabled

## Quick Start (Local Development)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/gemini-live-trading-agent.git
cd gemini-live-trading-agent
```

### 2. Set up Google Cloud credentials

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

### 3. Enable Vertex AI API

```bash
gcloud services enable aiplatform.googleapis.com
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Set environment variables

```bash
export PROJECT_ID="your-gcp-project-id"
export LOCATION="us-central1"
export MODEL="gemini-live-2.5-flash-native-audio"
```

### 6. Run the server

```bash
python -m src.main
```

Open [http://localhost:8080](http://localhost:8080) in your browser, click the microphone, and start talking.

## Deploy to Google Cloud Run

### Automated deployment

```bash
chmod +x deploy/deploy.sh
./deploy/deploy.sh YOUR_PROJECT_ID us-central1
```

### Manual deployment

```bash
# Build and push container
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/gemini-live-trading-agent

# Deploy to Cloud Run
gcloud run deploy gemini-live-trading-agent \
    --image gcr.io/YOUR_PROJECT_ID/gemini-live-trading-agent \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars "PROJECT_ID=YOUR_PROJECT_ID,LOCATION=us-central1,MODEL=gemini-live-2.5-flash-native-audio" \
    --memory 512Mi \
    --session-affinity
```

### Verify deployment

```bash
curl https://YOUR_SERVICE_URL/api/health
# {"status":"ok","service":"gemini-live-trading-agent"}
```

## Project Structure

```
1-live-agents/
  public/
    index.html          # Frontend (mic capture, audio playback, transcript)
  src/
    main.py             # FastAPI server + WebSocket endpoint
    config.py           # Configuration (env vars, trading pairs, voice)
    agents/
      live_trader.py    # Gemini Live session manager
    tools/
      market_tools.py   # 5 trading tools (price, TA, risk, alerts, overview)
  deploy/
    deploy.sh           # Automated Cloud Run deployment
    cleanup.sh          # Cleanup script
  docs/
    architecture.md     # Architecture diagram
  Dockerfile            # Cloud Run container
  requirements.txt      # Python dependencies
```

## How It Works

1. **User clicks microphone** — browser captures audio at 16kHz PCM16
2. **Audio streams via WebSocket** — binary frames sent to FastAPI server
3. **FastAPI proxies to Gemini Live API** — using `google-genai` SDK's `client.aio.live.connect()`
4. **Gemini processes speech** — understands intent, calls tools when needed
5. **Tools fetch real data** — CCXT queries Binance for live prices, OHLCV, etc.
6. **Gemini speaks back** — audio response streamed back through WebSocket to browser
7. **Transcripts displayed** — both user speech and agent responses shown in UI

## Example Voice Commands

- "How's Bitcoin doing?"
- "Give me the full picture on Ethereum"
- "What are the top movers right now?"
- "What's the risk if I put 5000 dollars in Solana?"
- "Set an alert for Bitcoin above 100k"
- "Compare ETH and SOL"

## Tech Stack

- **AI**: Gemini 2.5 Flash (Native Audio) via Vertex AI
- **SDK**: Google GenAI SDK (`google-genai>=1.44.0`)
- **Backend**: Python 3.12, FastAPI, uvicorn
- **Frontend**: Vanilla HTML/JS, Web Audio API, WebSocket
- **Market Data**: CCXT (Binance async)
- **Hosting**: Google Cloud Run
- **Container**: Docker

## Built for

[Gemini Live Agent Challenge](https://devpost.com/) — Category: Live Agents

## License

MIT

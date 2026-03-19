# Sentinel — Live Trading Agent

> **EN** | [FR](#version-française)
>
> ![Python](https://img.shields.io/badge/python-3.12-green)
> ![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash_Live-blue)
> ![CCXT](https://img.shields.io/badge/market_data-Binance_CCXT-yellow)
> ![Cloud](https://img.shields.io/badge/Google_Cloud-Run-orange)
> ![License](https://img.shields.io/badge/license-MIT-brightgreen)
>
> Real-time voice-powered cryptocurrency trading assistant built with **Gemini Live API** on Google Cloud. Speak naturally to get live prices, technical analysis, risk assessments, and market overviews — all through voice interaction.
>
> **Built for**: Gemini Live Agent Challenge — Category: Live Agents
>
> ---
>
> ## Table of Contents
>
> 1. [Overview](#overview)
> 2. 2. [Architecture](#architecture)
>    3. 3. [Features](#features)
>       4. 4. [Google Cloud Services](#google-cloud-services)
>          5. 5. [Quick Start](#quick-start)
>             6. 6. [Deploy to Cloud Run](#deploy-to-cloud-run)
>                7. 7. [Project Structure](#project-structure)
>                   8. 8. [How It Works](#how-it-works)
>                      9. 9. [Voice Commands](#voice-commands)
>                         10. 10. [Tech Stack](#tech-stack)
>                             11. 11. [Version Française](#version-française)
>                                
>                                 12. ---
>                                
>                                 13. ## Overview
>                                
>                                 14. Sentinel is a voice-first cryptocurrency trading assistant. Say "How's Bitcoin doing?" and get a complete spoken analysis — current price, RSI, MACD, volatility, risk score, and position recommendations — in real time via Binance market data.
>
> ---
>
> ## Architecture
>
> ```
> Browser (Mic / Speaker / Transcript)
>               |
>          WebSocket
>               |
>     Cloud Run (FastAPI)
>               |
>       Gemini Live API
>    (Gemini 2.5 Flash Native Audio)
>               |
>        CCXT / Binance
>       (Live Market Data)
> ```
>
> ---
>
> ## Features
>
> - **Voice-first**: Speak naturally, get spoken responses with data
> - - **Live market data**: Real-time prices from Binance via CCXT
>   - - **Technical analysis**: RSI, MACD, SMA, volatility indicators
>     - - **Risk assessment**: VaR calculation, risk scoring, position recommendations
>       - - **Price alerts**: Set voice-triggered price alerts
>         - - **Market overview**: Top movers and market summary
>           - - **Interruption handling**: Cut the agent off mid-sentence, it stops immediately
>            
>             - ---
>
> ## Google Cloud Services
>
> | Service | Usage |
> |---------|-------|
> | **Vertex AI** | Gemini Live API — bidirectional audio streaming with function calling |
> | **Cloud Run** | Hosts the FastAPI WebSocket server and static frontend |
> | **Cloud Build** | Builds the Docker container image |
> | **Container Registry** | Stores the container image |
>
> ---
>
> ## Quick Start
>
> ```bash
> # 1. Clone
> git clone https://github.com/Turbo31150/gemini-live-trading-agent.git
> cd gemini-live-trading-agent
>
> # 2. Google Cloud credentials
> gcloud auth application-default login
> gcloud config set project YOUR_PROJECT_ID
> gcloud services enable aiplatform.googleapis.com
>
> # 3. Install dependencies
> pip install -r requirements.txt
>
> # 4. Environment variables
> export PROJECT_ID="your-gcp-project-id"
> export LOCATION="us-central1"
> export MODEL="gemini-live-2.5-flash-native-audio"
>
> # 5. Run
> python -m src.main
> ```
>
> Open `http://localhost:8080`, click the microphone, and start talking.
>
> ---
>
> ## Deploy to Cloud Run
>
> ```bash
> # Automated
> chmod +x deploy/deploy.sh
> ./deploy/deploy.sh YOUR_PROJECT_ID us-central1
>
> # Verify
> curl https://YOUR_SERVICE_URL/api/health
> # {"status":"ok","service":"gemini-live-trading-agent"}
> ```
>
> ---
>
> ## Project Structure
>
> ```
> gemini-live-trading-agent/
> ├── public/
> │   └── index.html           # Frontend (mic capture, audio playback, transcript)
> ├── src/
> │   ├── main.py              # FastAPI server + WebSocket endpoint
> │   ├── config.py            # Configuration (env vars, trading pairs, voice)
> │   └── agents/
> │       └── live_trader.py   # Gemini Live session manager
> │   └── tools/
> │       └── market_tools.py  # 5 trading tools
> ├── deploy/
> │   ├── deploy.sh            # Automated Cloud Run deployment
> │   └── cleanup.sh           # Cleanup script
> ├── docs/
> │   └── architecture.md      # Architecture diagram
> ├── Dockerfile               # Cloud Run container
> └── requirements.txt         # Python dependencies
> ```
>
> ### 5 Trading Tools
>
> | Tool | Description |
> |------|-------------|
> | `get_price` | Real-time price + 24h change from Binance |
> | `get_technical_analysis` | RSI, MACD, SMA, volatility indicators |
> | `assess_risk` | VaR calculation, risk scoring, position recommendation |
> | `set_price_alert` | Voice-triggered price alert |
> | `get_market_overview` | Top movers + market summary |
>
> ---
>
> ## How It Works
>
> 1. User clicks microphone — browser captures audio at 16kHz PCM16
> 2. 2. Audio streams via WebSocket — binary frames sent to FastAPI server
>    3. 3. FastAPI proxies to Gemini Live API — using `google-genai` SDK's `client.aio.live.connect()`
>       4. 4. Gemini processes speech — understands intent, calls tools when needed
>          5. 5. Tools fetch real data — CCXT queries Binance for live prices, OHLCV, etc.
>             6. 6. Gemini speaks back — audio response streamed back through WebSocket to browser
>                7. 7. Transcripts displayed — both user speech and agent responses shown in UI
>                  
>                   8. ---
>                  
>                   9. ## Voice Commands
>                  
>                   10. ```
> "How's Bitcoin doing?"
> "Give me the full picture on Ethereum"
> "What are the top movers right now?"
> "What's the risk if I put 5000 dollars in Solana?"
> "Set an alert for Bitcoin above 100k"
> "Compare ETH and SOL"
> "What's the RSI on XRP?"
> ```
>
> ---
>
> ## Tech Stack
>
> | Layer | Technology |
> |-------|-----------|
> | **AI** | Gemini 2.5 Flash (Native Audio) via Vertex AI |
> | **SDK** | Google GenAI SDK (google-genai >= 1.44.0) |
> | **Backend** | Python 3.12, FastAPI, uvicorn |
> | **Frontend** | Vanilla HTML/JS, Web Audio API, WebSocket |
> | **Market Data** | CCXT (Binance async) |
> | **Hosting** | Google Cloud Run |
> | **Container** | Docker |
>
> ---
>
> *Author: Turbo31150 | Challenge: Gemini Live Agent Challenge | Category: Live Agents | License: MIT*
>
> ---
> ---
>
> # Version Française
>
> > [EN](#sentinel--live-trading-agent) | **FR**
>
> ![Python](https://img.shields.io/badge/python-3.12-green)
> ![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash_Live-blue)
> ![CCXT](https://img.shields.io/badge/données-Binance_CCXT-yellow)
> ![Cloud](https://img.shields.io/badge/Google_Cloud-Run-orange)
> ![Licence](https://img.shields.io/badge/licence-MIT-brightgreen)
>
> Assistant de trading de cryptomonnaies en temps réel piloté par la voix, construit avec **Gemini Live API** sur Google Cloud. Parlez naturellement pour obtenir les prix en direct, l'analyse technique, les évaluations de risque et les aperçus du marché — tout par interaction vocale.
>
> **Conçu pour** : Gemini Live Agent Challenge — Catégorie : Live Agents
>
> ---
>
> ## Table des matières FR
>
> 1. [Vue d'ensemble](#vue-densemble-fr)
> 2. [Architecture](#architecture-fr)
> 3. [Fonctionnalités](#fonctionnalités-fr)
> 4. [Services Google Cloud](#services-google-cloud-fr)
> 5. [Démarrage rapide](#démarrage-rapide-fr)
> 6. [Déploiement Cloud Run](#déploiement-cloud-run-fr)
> 7. [Structure du projet](#structure-du-projet-fr)
> 8. [Fonctionnement](#fonctionnement)
> 9. [Commandes vocales](#commandes-vocales-fr)
> 10. [Stack technique](#stack-technique-fr)
>
> ---
>
> ## Vue d'ensemble FR
>
> Sentinel est un assistant de trading de cryptomonnaies axé sur la voix. Dites "Comment va le Bitcoin ?" et obtenez une analyse parlée complète — prix actuel, RSI, MACD, volatilité, score de risque et recommandations de position — en temps réel via les données de marché Binance.
>
> ---
>
> ## Architecture FR
>
> ```
> Navigateur (Micro / Haut-parleur / Transcript)
>               |
>          WebSocket
>               |
>     Cloud Run (FastAPI)
>               |
>       Gemini Live API
>   (Gemini 2.5 Flash Audio Natif)
>               |
>        CCXT / Binance
>     (Données de marché Live)
> ```
>
> ---
>
> ## Fonctionnalités FR
>
> - **Voix en priorité** : Parlez naturellement, obtenez des réponses parlées avec données
> - **Données marché live** : Prix en temps réel depuis Binance via CCXT
> - **Analyse technique** : RSI, MACD, SMA, indicateurs de volatilité
> - **Évaluation du risque** : Calcul VaR, score de risque, recommandations de position
> - **Alertes de prix** : Alertes déclenchées par la voix
> - **Aperçu du marché** : Meilleures progressions et résumé du marché
> - **Interruption** : Coupez l'agent en pleine phrase, il s'arrête immédiatement
>
> ---
>
> ## Services Google Cloud FR
>
> | Service | Usage |
> |---------|-------|
> | **Vertex AI** | Gemini Live API — streaming audio bidirectionnel avec function calling |
> | **Cloud Run** | Héberge le serveur WebSocket FastAPI et le frontend statique |
> | **Cloud Build** | Construit l'image Docker du conteneur |
> | **Container Registry** | Stocke l'image du conteneur |
>
> ---
>
> ## Démarrage rapide FR
>
> ```bash
> # 1. Cloner
> git clone https://github.com/Turbo31150/gemini-live-trading-agent.git
> cd gemini-live-trading-agent
>
> # 2. Credentials Google Cloud
> gcloud auth application-default login
> gcloud config set project YOUR_PROJECT_ID
> gcloud services enable aiplatform.googleapis.com
>
> # 3. Installer les dépendances
> pip install -r requirements.txt
>
> # 4. Variables d'environnement
> export PROJECT_ID="votre-projet-gcp"
> export LOCATION="us-central1"
> export MODEL="gemini-live-2.5-flash-native-audio"
>
> # 5. Lancer
> python -m src.main
> ```
>
> Ouvrez `http://localhost:8080`, cliquez sur le micro et commencez à parler.
>
> ---
>
> ## Déploiement Cloud Run FR
>
> ```bash
> # Automatisé
> chmod +x deploy/deploy.sh
> ./deploy/deploy.sh YOUR_PROJECT_ID us-central1
>
> # Vérification
> curl https://YOUR_SERVICE_URL/api/health
> # {"status":"ok","service":"gemini-live-trading-agent"}
> ```
>
> ---
>
> ## Structure du projet FR
>
> ```
> gemini-live-trading-agent/
> ├── public/
> │   └── index.html           # Frontend (capture micro, lecture audio, transcript)
> ├── src/
> │   ├── main.py              # Serveur FastAPI + endpoint WebSocket
> │   ├── config.py            # Configuration (env vars, paires trading, voix)
> │   └── agents/
> │       └── live_trader.py   # Gestionnaire de session Gemini Live
> │   └── tools/
> │       └── market_tools.py  # 5 outils de trading
> ├── deploy/
> │   ├── deploy.sh            # Déploiement Cloud Run automatisé
> │   └── cleanup.sh           # Script de nettoyage
> ├── docs/
> │   └── architecture.md      # Schéma d'architecture
> ├── Dockerfile               # Conteneur Cloud Run
> └── requirements.txt         # Dépendances Python
> ```
>
> ### 5 outils de trading
>
> | Outil | Description |
> |-------|-------------|
> | `get_price` | Prix en temps réel + variation 24h depuis Binance |
> | `get_technical_analysis` | RSI, MACD, SMA, indicateurs de volatilité |
> | `assess_risk` | Calcul VaR, score de risque, recommandation de position |
> | `set_price_alert` | Alerte de prix déclenchée par la voix |
> | `get_market_overview` | Meilleures progressions + résumé du marché |
>
> ---
>
> ## Fonctionnement
>
> 1. L'utilisateur clique sur le micro — le navigateur capture l'audio en PCM16 16kHz
> 2. 2. L'audio est streamé via WebSocket — trames binaires envoyées au serveur FastAPI
>    3. 3. FastAPI proxie vers Gemini Live API — via `client.aio.live.connect()` du SDK `google-genai`
>       4. 4. Gemini traite la parole — comprend l'intention, appelle les outils si nécessaire
>          5. 5. Les outils récupèrent les données réelles — CCXT interroge Binance pour les prix live, OHLCV, etc.
>             6. 6. Gemini répond vocalement — réponse audio streamée via WebSocket vers le navigateur
>                7. 7. Les transcripts s'affichent — parole utilisateur et réponses de l'agent dans l'interface
>                  
>                   8. ---
>                  
>                   9. ## Commandes vocales FR
>                  
>                   10. ```
> "Comment va le Bitcoin ?"
> "Donne-moi l'analyse complète d'Ethereum"
> "Quels sont les meilleurs performers en ce moment ?"
> "Quel est le risque si je mets 5000 euros en Solana ?"
> "Mets une alerte quand Bitcoin dépasse 100k"
> "Compare ETH et SOL"
> "Quel est le RSI du XRP ?"
> ```
>
> ---
>
> ## Stack technique FR
>
> | Couche | Technologie |
> |--------|-------------|
> | **IA** | Gemini 2.5 Flash (Audio Natif) via Vertex AI |
> | **SDK** | Google GenAI SDK (google-genai >= 1.44.0) |
> | **Backend** | Python 3.12, FastAPI, uvicorn |
> | **Frontend** | Vanilla HTML/JS, Web Audio API, WebSocket |
> | **Données marché** | CCXT (Binance async) |
> | **Hébergement** | Google Cloud Run |
> | **Conteneur** | Docker |
>
> ---
>
> *Auteur : Turbo31150 | Challenge : Gemini Live Agent Challenge | Catégorie : Live Agents | Licence : MIT*

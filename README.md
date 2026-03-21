<div align="center">
  <img src="assets/logo.svg" alt="GEMINI·LIVE·TRADER" width="520"/>
  <br/><br/>

  [![License: MIT](https://img.shields.io/badge/License-MIT-34D399?style=flat-square)](LICENSE)
  [![Python](https://img.shields.io/badge/Python-3.11+-34D399?style=flat-square&logo=python&logoColor=black)](#)
  [![Gemini](https://img.shields.io/badge/Gemini_Live_API-Google_Cloud-4285F4?style=flat-square&logo=google)](#)
  [![Voice](https://img.shields.io/badge/Voice-trading_orders-FBBF24?style=flat-square)](#)

  <br/>
  <p><strong>Assistant trading vocal temps réel · Gemini Live API · Ordres vocaux · Marchés live · Google Cloud</strong></p>
  <p><em>Passez des ordres de trading par la voix — Gemini analyse les marchés en temps réel et exécute vos stratégies</em></p>
</div>

---

## Présentation

**GEMINI·LIVE·TRADER** est un assistant de trading vocal construit sur la **Gemini Live API**. Il permet de passer des ordres, analyser des marchés et gérer des positions entièrement par commandes vocales — avec analyse IA en temps réel propulsée par Gemini.

---

## Fonctionnalités

| Feature | Description |
|---------|-------------|
| **Commandes vocales** | "Achète 0.1 BTC au marché" → ordre exécuté |
| **Analyse temps réel** | Gemini analyse prix, volume, momentum |
| **Questions marché** | "Quel est le RSI BTC sur 4h ?" → réponse vocale |
| **Alertes** | Notifications vocales sur événements marchés |
| **Rapport portefeuille** | "Montre mon PnL" → synthèse vocale |

---

## Architecture

```
Microphone → Gemini Live API (STT + LLM + TTS)
                    │
              Intent Parser
              ├── MARKET_DATA → fetch price/volume
              ├── PLACE_ORDER → exécution API
              ├── PORTFOLIO  → positions PnL
              └── ANALYSIS   → TA + résumé
                    │
              Execution Layer (Exchange API)
                    │
              Réponse vocale (TTS Gemini)
```

---

## Installation

```bash
git clone https://github.com/Turbo31150/gemini-live-trading-agent.git
cd gemini-live-trading-agent
pip install -r requirements.txt
export GOOGLE_API_KEY=AIza...
export EXCHANGE_API_KEY=...
python main.py
```

---

<div align="center">

**Franc Delmas (Turbo31150)** · Google Cloud · Gemini Live API · MIT License

</div>

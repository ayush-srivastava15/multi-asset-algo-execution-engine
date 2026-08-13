# ⚡ Universal Multi-Broker & Multi-Asset Low-Latency Execution Engine

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Infrastructure](https://img.shields.io/badge/AWS-EC2%20(ap--south--1)-orange.svg)](https://aws.amazon.com/)
[![Latency](https://img.shields.io/badge/Latency-Sub--100ms-red.svg)](#)

A high-frequency event-driven algorithmic trading execution engine built in Python. Designed for deployment on **AWS EC2 (Mumbai Region)** with sub-second REST polling latency. Supports multi-broker routing (**Angel One, Zerodha, Dhan**) across diverse asset classes (**Nifty 50, BankNifty, Equity Stocks**).

---

## 🏗️ System Architecture

```text
                  ┌──────────────────────────────────────────┐
                  │          Live Market Price Feed          │
                  └────────────────────┬─────────────────────┘
                                       │
                                 [100ms Tick]
                                       │
                                       ▼
                  ┌──────────────────────────────────────────┐
                  │       Universal Execution Engine         │
                  │        (AWS EC2 - ap-south-1)            │
                  └────────────┬────────────────┬────────────┘
                               │                │
            ┌──────────────────┘                └──────────────────┐
            ▼                                                      ▼
┌───────────────────────┐                                ┌───────────────────┐
│ Pluggable Strategy    │                                │  Broker Abstraction│
│ Interface (ORB Engine)│                                │      Adapter      │
└───────────────────────┘                                └─────────┬─────────┘
                                                                   │
                                                ┌──────────────────┼──────────────────┐
                                                ▼                  ▼                  ▼
                                         ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
                                         │  Angel One  │    │   Zerodha   │    │    Dhan     │
                                         └─────────────┘    └─────────────┘    └─────────────┘
✨ Key FeaturesBroker-Agnostic Architecture: Features an abstraction adapter layer allowing instant broker switching (Angel One, Zerodha, Dhan) without modifying core engine logic.Multi-Asset Compatibility: Fully dynamic parameters for Index Derivatives (Nifty 50, BankNifty, FinNifty) and High-Beta Equity Stocks.Decoupled Strategy Module: Complete isolation of signal generation from order routing. Comes with a default Morning Opening Range Breakout (ORB) strategy.AWS Server Time Sync: Timezone-aware engine handling UTC-to-IST offsets (03:45:00 UTC = 09:15:00 IST) for seamless cloud execution.Sub-Second Polling (100ms): Optimized polling engine designed to catch opening market volatility within milliseconds.Persistent Audit Logging: Automatic structured time-series CSV logging for execution prices, signal types, and timestamps.🛠️ Tech StackDomainTechnologiesLanguagePython 3.10+Broker APIsAngel One SmartAPI, Pluggable API AdaptersCloud & InfraAWS EC2 (Ubuntu 22.04 LTS), Linux Screen DaemonData & AuthPandas, PyOTP, Python-Dotenv📁 Repository StructurePlaintext.
├── config.py                 # Multi-Broker & Instrument Configurations
├── strategy_interface.py    # Decoupled Strategy Base & ORB Engine
├── algo_engine.py           # Core High-Speed Execution Engine
├── .env.example             # API Credentials Template
├── .gitignore               # Excludes secrets & CSV logs
├── requirements.txt         # Project Dependencies
└── README.md                # System Documentation
🚀 AWS EC2 Deployment Guide1. Connect to Cloud InstanceBashssh -i "your-aws-key.pem" ubuntu@your-ec2-ip
2. Clone Repository & Install DependenciesBashgit clone [https://github.com/ayush-srivastava15/multi-asset-algo-execution-engine.git](https://github.com/ayush-srivastava15/multi-asset-algo-execution-engine.git)
cd multi-asset-algo-execution-engine
pip install -r requirements.txt
3. Environment SetupCreate and configure your .env file:Bashcp .env.example .env
nano .env
4. Run Headless via Linux ScreenBash# Start background screen session
screen -S algo_engine

# Run Execution Engine
python3 algo_engine.py

# Detach session (Keep running in background): Press Ctrl + A, then D
🔒 Security & Best PracticesZero Credential Exposure: Environment variables are enforced via python-dotenv and ignored by .gitignore.IP Protection: Proprietary execution logic is decoupled from public API wrappers.👨‍💻 AuthorAyush SrivastavaGitHub: @ayush-srivastava15Role: Quant Developer / Algorithmic Systems Engineer
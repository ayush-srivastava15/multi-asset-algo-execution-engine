import os
from dotenv import load_dotenv

load_dotenv()

# Broker Selection & Credentials
ACTIVE_BROKER = "ANGEL_ONE"  # Options: ANGEL_ONE, ZERODHA, DHAN

BROKER_CREDENTIALS = {
    "ANGEL_ONE": {
        "API_KEY": os.getenv("ANGEL_API_KEY", "YOUR_API_KEY"),
        "CLIENT_ID": os.getenv("ANGEL_CLIENT_ID", "YOUR_CLIENT_ID"),
        "PASSWORD": os.getenv("ANGEL_PASSWORD", "YOUR_MPIN")
    }
}

# Target Instrument Configuration (Can be Nifty, BankNifty, or Stocks)
INSTRUMENT_CONFIG = {
    "SYMBOL": "Nifty 50",         # Example: Nifty 50, Bank Nifty, RELIANCE
    "TOKEN": "99926000",          # Instrument Token
    "EXCHANGE": "NSE",            # NSE, NFO, BSE
    "LOT_SIZE": 50                # Qty per order
}

# System Settings
POLL_INTERVAL = 0.1  # 100ms sub-second polling latency
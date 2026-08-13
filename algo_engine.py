# algo_engine.py - Universal Execution Engine
import time
import os
import pandas as pd
from datetime import datetime
from SmartApi import SmartConnect

import config
from strategy_interface import MorningBreakoutStrategy

class BrokerAdapter:
    """
    Abstraction Layer to support Multiple Brokers (Angel One, Zerodha, Dhan, etc.)
    """
    def __init__(self, broker_name):
        self.broker_name = broker_name
        self.api = None

    def connect(self):
        if self.broker_name == "ANGEL_ONE":
            creds = config.BROKER_CREDENTIALS["ANGEL_ONE"]
            self.api = SmartConnect(api_key=creds["API_KEY"])
            totp = input("🔑 Enter Mobile TOTP for Angel One: ")
            session = self.api.generateSession(creds["CLIENT_ID"], creds["PASSWORD"], totp)
            return session.get('status', False)
        # Extendable for Zerodha / Dhan / Upstox APIs
        return False

    def fetch_ltp(self, exchange, symbol, token):
        if self.broker_name == "ANGEL_ONE":
            try:
                data = self.api.ltpData(exchange, symbol, token)
                return float(data['data']['ltp'])
            except Exception:
                return None
        return None


class UniversalAlgoEngine:
    def __init__(self, strategy_instance):
        self.broker = BrokerAdapter(config.ACTIVE_BROKER)
        self.strategy = strategy_instance
        self.trade_log = []

    def log_event(self, action, strike_type, spot_price, remarks):
        t = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"👉 [{t}] | {action:<4} | {strike_type:<10} | Price: {spot_price:<8} | {remarks}")
        self.trade_log.append({"Time": t, "Action": action, "Price": spot_price, "Remarks": remarks})
        try:
            filename = f"Execution_Log_{datetime.now().strftime('%Y%m%d')}.csv"
            pd.DataFrame(self.trade_log).to_csv(filename, index=False)
        except Exception:
            pass

    def start(self):
        print(f"⚡ Initializing Execution Engine for [{config.INSTRUMENT_CONFIG['SYMBOL']}]...")
        if not self.broker.connect():
            print("❌ Broker Authentication Failed.")
            return

        print("✅ Broker Connected Successfully! Monitoring Market Feeds...")

        inst = config.INSTRUMENT_CONFIG

        while not self.strategy.state["day_done"]:
            try:
                time.sleep(config.POLL_INTERVAL)
                ltp = self.broker.fetch_ltp(inst["EXCHANGE"], inst["SYMBOL"], inst["TOKEN"])
                if ltp is None:
                    continue

                # Lock Opening Price (03:45:00 UTC = 09:15:00 IST for AWS EC2 Instances)
                current_utc = datetime.now().strftime("%H:%M:%S")
                if current_utc >= "03:45:00" and self.strategy.open_price is None:
                    self.strategy.set_open_price(ltp)
                    self.log_event("INFO", "OPEN", ltp, f"Open Price Locked for {inst['SYMBOL']}: {ltp}")

                if self.strategy.open_price is None:
                    continue

                # Process Strategy Logic
                signal = self.strategy.evaluate(ltp)
                if signal:
                    action, strike_type, remarks = signal
                    self.log_event(action, strike_type, ltp, remarks)

            except Exception as e:
                continue

        print("🎉 Execution Completed Successfully!")

if __name__ == "__main__":
    # Pluggable Morning Strategy Example (Configurable for Nifty/BankNifty/Stocks)
    orb_strategy = MorningBreakoutStrategy(breakout_threshold=15.0, target_pts=30.0, stop_loss_pts=15.0)
    
    # Run Universal Engine
    engine = UniversalAlgoEngine(strategy_instance=orb_strategy)
    engine.start()
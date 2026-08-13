class BaseStrategy:
    """
    Abstract Generic Strategy Interface.
    Can be inherited for any Custom Asset Class (Equities, Index Derivatives, Forex).
    """
    def __init__(self, name="Generic Asset Strategy"):
        self.name = name
        self.open_price = None
        self.state = {
            "position": None,
            "entry_price": 0.0,
            "day_done": False
        }

    def set_open_price(self, price):
        self.open_price = price

    def evaluate(self, current_price):
        raise NotImplementedError("Subclasses must implement evaluate()")


class MorningBreakoutStrategy(BaseStrategy):
    """
    Standard Morning Opening Range Breakout (ORB) Strategy.
    Triggers LONG when price crosses Open + Threshold, SHORT when price crosses Open - Threshold.
    Applicable across Nifty, BankNifty, and High-Beta Stocks.
    """
    def __init__(self, breakout_threshold=15.0, target_pts=30.0, stop_loss_pts=15.0):
        super().__init__(name="Morning ORB Multi-Asset Strategy")
        self.threshold = breakout_threshold
        self.target = target_pts
        self.sl = stop_loss_pts

    def evaluate(self, ltp):
        if self.state["day_done"] or self.open_price is None:
            return None

        O = self.open_price

        # 1. Entry Condition (Breakout above/below opening price)
        if self.state["position"] is None:
            if ltp >= (O + self.threshold):
                self.state["position"] = "BUY_CE"
                self.state["entry_price"] = ltp
                return ("BUY", "CALL", f"Bullish ORB Breakout triggered at {ltp}")
            elif ltp <= (O - self.threshold):
                self.state["position"] = "BUY_PE"
                self.state["entry_price"] = ltp
                return ("BUY", "PUT", f"Bearish ORB Breakout triggered at {ltp}")

        # 2. Risk Management (Target & Stop Loss Checks)
        else:
            entry = self.state["entry_price"]
            pos = self.state["position"]

            # Target Check
            if (pos == "BUY_CE" and ltp >= entry + self.target) or \
               (pos == "BUY_PE" and ltp <= entry - self.target):
                self.state["day_done"] = True
                return ("EXIT", "ALL", f"Target Hit ({self.target} pts) 🎯 at {ltp}")

            # Stop Loss Check
            if (pos == "BUY_CE" and ltp <= entry - self.sl) or \
               (pos == "BUY_PE" and ltp >= entry + self.sl):
                self.state["day_done"] = True
                return ("EXIT", "ALL", f"Stop Loss Hit ({self.sl} pts) 🛑 at {ltp}")

        return None
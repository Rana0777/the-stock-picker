class MomentumStrategy:
    def __init__(self, window_size=14):
        self.window_size = window_size

    def calculate_signals(self, price_data):
        signals = []
        for i in range(len(price_data)):
            if i < self.window_size:
                signals.append(0)
            else:
                momentum = price_data[i] - price_data[i - self.window_size]
                signals.append(1 if momentum > 0 else -1)
        return signals

    def generate_trade_decision(self, signals):
        if signals[-1] == 1:
            return "BUY"
        elif signals[-1] == -1:
            return "SELL"
        else:
            return "HOLD"
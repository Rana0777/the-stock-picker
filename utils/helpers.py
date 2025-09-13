def log_message(message):
    print(f"[LOG] {message}")

def calculate_returns(prices):
    if len(prices) < 2:
        return []
    returns = [(prices[i] - prices[i - 1]) / prices[i - 1] for i in range(1, len(prices))]
    return returns
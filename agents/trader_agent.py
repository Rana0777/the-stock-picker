class TraderAgent:
    def __init__(self, strategy):
        self.strategy = strategy
        self.balance = 100000  # Initial balance
        self.position = 0  # Current position in the market

    def initialize(self):
        # Initialize the agent with necessary parameters
        print("TraderAgent initialized with strategy:", self.strategy)

    def execute_trade(self, market_data):
        # Execute a trade based on the selected strategy
        decision = self.strategy.generate_trade_decision(market_data)
        if decision == "buy":
            self.position += 1
            self.balance -= market_data['price']
            print("Executed Buy: Current Position:", self.position, "Balance:", self.balance)
        elif decision == "sell" and self.position > 0:
            self.position -= 1
            self.balance += market_data['price']
            print("Executed Sell: Current Position:", self.position, "Balance:", self.balance)

    def evaluate_performance(self):
        # Evaluate the performance of the trading agent
        return self.balance + (self.position * market_data['price'])  # Example performance metric
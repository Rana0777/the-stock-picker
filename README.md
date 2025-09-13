# Autonomous Stock Market Agentic System (AI Hedge Fund Lite)

## Overview
AI Hedge Fund Lite is an autonomous stock market agentic system designed to implement trading strategies using the CrewAI framework. This project aims to provide a lightweight and efficient platform for algorithmic trading, focusing on momentum-based strategies.

## Project Structure
```
ai-hedge-fund-lite
├── src
│   ├── main.py                # Entry point of the application
│   ├── agents
│   │   └── trader_agent.py    # Trader agent responsible for executing trades
│   ├── strategies
│   │   └── momentum_strategy.py # Implements momentum-based trading strategy
│   ├── data
│   │   └── data_loader.py      # Loads and preprocesses market data
│   ├── crewai_config
│   │   └── config.yaml         # Configuration settings for CrewAI framework
│   └── utils
│       └── helpers.py          # Utility functions for various operations
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Files and directories to ignore in version control
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd ai-hedge-fund-lite
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the CrewAI settings in `src/crewai_config/config.yaml` as needed.

## Usage Guidelines
- To run the application, execute the following command:
  ```
  python src/main.py
  ```

- The system will initialize the CrewAI framework and start executing the trading agents based on the defined strategies.

## System Architecture
The architecture of AI Hedge Fund Lite consists of several components:
- **Agents**: Responsible for executing trades based on strategies.
- **Strategies**: Define the logic for making trading decisions.
- **Data**: Handles the loading and preprocessing of market data.
- **Utilities**: Provide helper functions for logging and calculations.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
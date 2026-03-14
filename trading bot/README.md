# Binance Futures Testnet Trading Bot (Pro Version)

A modular Python CLI application for executing MARKET and LIMIT orders on the Binance Futures Testnet (USDT-M)[cite: 1]. This version features an advanced Rule Engine that automatically fetches exchange limits to ensure order success.

## Features
* **Automatic Data Cleaning**: Automatically rounds quantity and price to match Binance’s stepSize and tickSize requirements[cite: 1, 3].
* **Live Filter Fetching**: Dynamically retrieves symbol-specific rules, such as Minimum Notional and Precision, from the Binance exchange[cite: 3].
* **Safety Layer**: Prevents common "Filter Failure" and "API Error: -1111" by validating orders before they are sent[cite: 3].
* **Modular Design**: Separates API interaction, business logic, and command-line interface for reusability[cite: 1].
* **Structured Logging**: All requests, responses, and errors are captured in trading.log[cite: 1].

## Setup and Installation

### 1. Prerequisites
* Python 3.8+
* Binance Futures Testnet API Key and Secret

### 2. Installation
Clone the repository and install dependencies:
pip install -r requirements.txt [cite: 1]

### 3. Configuration
Create a .env file in the root directory and add your credentials[cite: 1, 2]:
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
take .env.example as an model for the creating file.

## Usage Examples

The bot now performs "soft rounding." If you provide a quantity with too many decimals, the bot will adjust it and inform you before execution.

### Place a Market Order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.0015 [cite: 1]

### Place a Limit Order
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.01 --price 60000 [cite: 1]

## How the  Validation Works
1. Fetch Rules: The bot calls the exchange to find out exactly what the symbol allows (e.g., decimal limits).
2. Clean Data: The OrderValidator rounds your input to the correct decimal precision (Step Size).
3. Notional Check: It calculates (Quantity * Price) to ensure the trade meets the minimum USDT threshold (e.g., $5.00).
4. Execute: Only sanitized and validated data is sent to the Binance API.

## Project Structure
* bot/client.py: Handles connection and fetches live exchange rules[cite: 1].
* bot/orders.py: Core logic for order construction and execution[cite: 1].
* bot/validators.py: Logic for verifying user input and rounding data[cite: 1].
* bot/logging_cfg.py: Configuration for dual-output logging (File + Console)[cite: 1].
* cli.py: The entry point that orchestrates cleaning and execution[cite: 1].

## Assumptions
* The bot is configured strictly for the USDT-M (USDT-Margined) Testnet[cite: 1].
* The user provides sufficient margin in their Testnet account for execution[cite: 1].
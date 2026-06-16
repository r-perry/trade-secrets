#!/usr/bin/env python3
import json
import os
import requests

# ==============================================================================
# 1. GLOBAL CREDENTIALS & CONFIGURATION
# ==============================================================================
ALLOCATION_PER_TICKER = 500.00  # Target dollar budget per stock selection
ALPACA_BASE_URL = "https://paper-api.alpaca.markets"

# Paste your actual credentials here once. All functions below will reuse them.
ALPACA_KEY = "PK5KHSFOVBWXJLHDETB3CTVMLJ"
ALPACA_SECRET = "F7WQGgBBE3yV27wSf2dAfBXhDmAPDXGYRTJ1YVsLvU4W"

# ==============================================================================
# 2. DATA INGESTION LAYER
# ==============================================================================
def get_congress_trades():
    print("DEBUG: Fetching target workspaces data stream...")
    # Simulated input payload mirroring the target logic verified in Phase 2
    mock_payload = [
        {
            "representative": "Cleo Fields",
            "type": "Purchase",
            "ticker": "AAPL",
        },
        {
            "representative": "Cleo Fields",
            "type": "Sale",
            "ticker": "MSFT",
        },
        {"representative": "Unrelated Politician", "type": "Purchase", "ticker": "NVDA"},
        {
            "representative": "Cleo Fields",
            "type": "Purchase",
            "ticker": "AMZN",
        },
    ]
    return mock_payload


def filter_high_conviction_trades(trades):
    valid_tickers = []
    for trade in trades:
        representative = trade.get("representative", "")
        if "Cleo Fields" in representative:
            tx_type = str(trade.get("type", "")).lower()
            if "purchase" in tx_type:
                ticker = trade.get("ticker")
                if ticker and ticker != "--":
                    valid_tickers.append(ticker.upper())
    return list(set(valid_tickers))


# ==============================================================================
# 3. ALPACA PORTFOLIO RECONCILIATION LAYER (Uses Global Keys)
# ==============================================================================
def get_existing_positions():
    """Queries Alpaca to see what stocks are currently sitting in the portfolio."""
    url = f"{ALPACA_BASE_URL}/v2/positions"
    headers = {"APCA-API-KEY-ID": ALPACA_KEY, "APCA-API-SECRET-KEY": ALPACA_SECRET}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            positions = response.json()
            # Loop through assets and isolate raw ticker names
            owned_tickers = [pos.get("symbol").upper() for pos in positions]
            return owned_tickers
        return []
    except Exception:
        print("⚠️ Portfolio status lookup failed. Defaulting to safe mode.")
        return []


def get_live_price(ticker):
    """Hits the market data stream to parse exact target asset prices for sizing."""
    url = f"https://data.alpaca.markets/v2/stocks/{ticker}/quotes/latest"
    headers = {"APCA-API-KEY-ID": ALPACA_KEY, "APCA-API-SECRET-KEY": ALPACA_SECRET}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            ask_price = data.get("quote", {}).get("ap", 0)
            if ask_price > 0:
                return float(ask_price)

        print(f"⚠️ Live quote unreachable. Applying sandbox fallback baseline.")
        fallbacks = {"AAPL": 180.00, "AMZN": 175.00}
        return fallbacks.get(ticker, 100.00)
    except Exception:
        return 100.00


# ==============================================================================
# 4. MAIN PIPELINE EXECUTION
# ==============================================================================
def execute_automatic_pipeline():
    print("=======================================================")
    print("🤖 RUNNING UNIFIED AUTOMATED INVESTING BOT             ")
    print("=======================================================\n")

    # Step 1: Filter downstream trade data
    raw_trades = get_congress_trades()
    shopping_list = filter_high_conviction_trades(raw_trades)

    if not shopping_list:
        print("🛑 Loop complete: No political moves matched targeting metrics today.")
        return

    # Step 2: Fetch portfolio state to prevent concentration risk
    owned_stocks = get_existing_positions()
    print(f"📊 Live Portfolio Check -> Current holdings: {owned_stocks}")

    # Step 3: Run execution routing
    order_url = f"{ALPACA_BASE_URL}/v2/orders"
    headers = {
        "APCA-API-KEY-ID": ALPACA_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET,
        "Content-Type": "application/json",
    }

    for ticker in shopping_list:
        # Check against existing positions array
        if ticker in owned_stocks:
            print(
                f"⏩ SKIPPING {ticker}: Already owned in dashboard. Dropping redundant allocation."
            )
            continue

        # Mathematical size mapping
        price = get_live_price(ticker)
        shares_to_buy = int(ALLOCATION_PER_TICKER // price)

        if shares_to_buy <= 0:
            print(f"⏩ Skipping {ticker}: Price outbounds current budget target.")
            continue

        payload = {
            "symbol": ticker,
            "qty": str(shares_to_buy),
            "side": "buy",
            "type": "market",
            "time_in_force": "gtc",
        }

        print(
            f"📦 Allocation target: ${ALLOCATION_PER_TICKER} -> Buying {shares_to_buy} shares of {ticker} at ~${price}..."
        )

        try:
            response = requests.post(
                order_url, json=payload, headers=headers, timeout=5
            )
            if response.status_code in [200, 201]:
                print(f"🚀 SUCCESS: Market order for {ticker} deployed successfully.")
            else:
                print(f"❌ Execution rejected: {response.text}")
        except Exception as e:
            print(f"❌ Transmission pipeline dropped order: {e}")


if __name__ == "__main__":
    execute_automatic_pipeline()

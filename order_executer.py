#!/usr/bin/env python3
import json
import os
import requests


def deploy_alpaca_orders(shopping_list):
    # Paper Trading Endpoint configuration
    base_url = "https://paper-api.alpaca.markets"
    order_url = f"{base_url}/v2/orders"

    # Pull credentials from the environment or default placeholders
    api_key = os.environ.get("ALPACA_API_KEY", "PK5KHSFOVBWXJLHDETB3CTVMLJ")
    secret_key = os.environ.get(
        "ALPACA_SECRET_KEY", "F7WQGgBBE3yV27wSf2dAfBXhDmAPDXGYRTJ1YVsLvU4W"
    )

    headers = {
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": secret_key,
        "Content-Type": "application/json",
    }

    print(f"\n=======================================================")
    print(f"🚀 INITIALIZING ALPACA TRADING DISPATCH LOOP...        ")
    print(f"=======================================================\n")

    for ticker in shopping_list:
        # Standard algorithmic market order payload
        payload = {
            "symbol": ticker,
            "qty": "5",  # Keep it simple: buying 5 shares of each target
            "side": "buy",
            "type": "market",
            "time_in_force": "gtc",  # Good 'Til Canceled
        }

        print(f"📦 Packaging Order Payload for {ticker}...")

        try:
            # We set a tight 3-second timeout so the script won't hang during local testing
            response = requests.post(
                order_url, json=payload, headers=headers, timeout=3
            )

            if response.status_code == 200 or response.status_code == 201:
                print(
                    f"✅ ORDER PLACED SUCCESSFULLY: 5 shares of {ticker} executed via Paper API."
                )
            else:
                print(
                    f"❌ Alpaca rejected order for {ticker}: Code {response.status_code} - {response.text}"
                )

        except requests.exceptions.RequestException:
            # NETWORK OFFLINE FALLBACK: Emulate and display the raw payload transmission
            print("⚠️ Network unreachable. Activating Sandbox Emulation Mode...")
            print("--- RAW OUTBOUND HTTP PACKET ---")
            print(f"POST {order_url} HTTP/1.1")
            print(f"Headers: {json.dumps(headers, indent=2)}")
            print(f"Body: {json.dumps(payload, indent=2)}")
            print("--------------------------------\n")


if __name__ == "__main__":
    # Pulling your validated target list from the Phase 2 output
    simulated_shopping_list = ["AAPL", "AMZN"]

    deploy_alpaca_orders(simulated_shopping_list)

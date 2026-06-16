#!/usr/bin/env python3
import json

def get_congress_trades():
    print("DEBUG: Simulating API Stream via Local Sandbox Payload...")
    
    # This mock dataset perfectly mimics a live JSON payload from a financial API.
    # It contains a valid target purchase, a sale we want to ignore, and an outside actor.
    mock_api_payload = [
        {
            "representative": "Cleo Fields",
            "type": "Purchase",
            "ticker": "AAPL",
            "amount": "$15,001 - $50,000"
        },
        {
            "representative": "Cleo Fields",
            "type": "Sale",
            "ticker": "MSFT",
            "amount": "$1,001 - $15,000"
        },
        {
            "representative": "Unrelated Politician",
            "type": "Purchase",
            "ticker": "NVDA",
            "amount": "$50,001 - $100,000"
        },
        {
            "representative": "Cleo Fields",
            "type": "Purchase",
            "ticker": "AMZN",
            "amount": "$1,001 - $15,000"
        }
    ]
    
    return mock_api_payload

def filter_high_conviction_trades(trades):
    valid_tickers = []
    matches_found = 0

    for trade in trades:
        representative = trade.get("representative", "")
        is_target_politician = "Cleo Fields" in representative
        
        if is_target_politician:
            matches_found += 1
            tx_type = str(trade.get("type", "")).lower()
            
            # CORE BUSINESS RULE: Isolate the target's BUY positions; completely drop the sales.
            if "purchase" in tx_type:
                ticker = trade.get("ticker")
                if ticker and ticker != "--":
                    valid_tickers.append(ticker.upper())

    print(f"DEBUG: Filter engine scanned mock payload and isolated {matches_found} matching records.")
    return list(set(valid_tickers))

if __name__ == "__main__":
    print("================================================")
    print("Running Local Mock Pipeline Engine inside VM... ")
    print("================================================")

    raw_data = get_congress_trades()
    shopping_list = filter_high_conviction_trades(raw_data)
    
    print(f"\n🚀 Complete Filtered Shopping List: {shopping_list}")

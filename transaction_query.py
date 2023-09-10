import json
import base64
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from algosdk.v2client import indexer

load_dotenv()

private_key_2 = os.getenv("TEST_ACCOUNT_PRIVATE_KEY")
address_2 = os.getenv("TEST_ACCOUNT_ADDRESS")
mnemonic_2 = os.getenv("TEST_ACCOUNT_MNEMONIC")

# Replace these variables with your indexer token and indexer address
indexer_address = "https://testnet-idx.algonode.cloud"
indexer_token = ""
headers = ""

# Create an instance of the IndexerClient
idx_client = indexer.IndexerClient(indexer_token, indexer_address, headers)

try:
    # Search for transactions for the specified account address
    current_time_rfc3339 = datetime.utcnow().isoformat() + "Z"

    # Get the current time
    current_time = datetime.utcnow()

    # Subtract 30 minutes
    time_30_minutes_ago = current_time - timedelta(minutes=30)

    # Format the time in RFC 3339 format
    time_30_minutes_ago_rfc3339 = time_30_minutes_ago.isoformat() + "Z"

    response = idx_client.search_transactions_by_address(
        address=address_2,
        limit=1,
        start_time=time_30_minutes_ago_rfc3339,
    )

    # Check if there are any transactions found
    if response and response.get("transactions"):
        latest_transaction = response["transactions"][0]  # Get the latest transaction

        # Decode and print the notes field if present
        notes = latest_transaction.get("note")
        if notes:
            decoded_notes = base64.b64decode(notes).decode("utf-8")
            print("Latest Transaction Notes:")
            print(decoded_notes)
        else:
            print("No notes found in the latest transaction.")

        # Print the entire transaction details
        print("\nLatest Transaction:")
        print(json.dumps(latest_transaction, indent=4))
    else:
        print("No transactions found for the specified account address.")
except Exception as e:
    print(f"An error occurred: {e}")
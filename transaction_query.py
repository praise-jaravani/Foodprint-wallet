import json
import base64
from dotenv import load_dotenv
import os
import time
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

def query():
    try:
        # Calculate the current time in RFC 3339 format
        current_time_rfc3339 = datetime.utcnow().isoformat() + "Z"

        # Calculate the time 60 seconds ago from the current time
        time_60_seconds_ago = datetime.utcnow() - timedelta(seconds=60)

        # Format the time 60 seconds ago in RFC 3339 format
        time_60_seconds_ago_rfc3339 = time_60_seconds_ago.isoformat() + "Z"

        response = idx_client.search_transactions_by_address(
            address=address_2,
            limit=1,
            start_time=time_60_seconds_ago_rfc3339,
            end_time=current_time_rfc3339,  # Set end_time to the current time
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
            #print("\nLatest Transaction:")
            #print(json.dumps(latest_transaction, indent=4))
        else:
            print("No new transactions found for the specified account address.")
    except Exception as e:
        print(f"An error occurred: {e}")

interval = 60

while True:
    # Call the function you want to run
    query()

    # Wait for the specified interval before running the code again
    time.sleep(interval)
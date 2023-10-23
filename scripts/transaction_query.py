import json
import base64
from dotenv import load_dotenv
import os
import time
from datetime import datetime, timedelta
from algosdk.v2client import indexer
import sqlite3

# Connect to the database
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

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

def query(time_60_seconds_ago_rfc3339, current_time_rfc3339):
    try:
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

            # Update Database
            # Get the current date and time
            current_datetime = datetime.now()

            # Format it as 'YYYY-MM-DD HH:MM:SS'
            formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            print("********** Transaction Table Information **********")
            # What is contained in the notes field. User and Transaction Information?
            user = decoded_notes
            print("User:",user)
            type_var = json.dumps(latest_transaction["tx-type"])
            print("Type:",type_var)
            logdatetime = formatted_datetime
            print("Time:",logdatetime)
            from_var = json.dumps(latest_transaction["sender"])
            print("From:",from_var)
            to_var = json.dumps(latest_transaction["payment-transaction"]["receiver"])
            print("To:",to_var)
            message = decoded_notes
            print("Message:", message)
            amount = json.dumps(latest_transaction["payment-transaction"]["amount"])
            print("Amount:", float(amount))
            valid = 1
            print("Valid:",valid)
            txhash = json.dumps(latest_transaction["id"])
            print("Txhash",txhash)

            # Check if a user exists in the database
            sql_query = "SELECT * FROM users WHERE tag = ?"

            # Execute the query with the specific_tag as a parameter
            cursor.execute(sql_query, (user,))

            # Fetch the result
            proof = cursor.fetchone()

            # Check if a user with the specific tag exists
            if proof is not None:
                pass
            else:
                print("Updating suspense account!")
                user = 00000

            transactions_data = [(user, type_var, logdatetime, from_var, to_var, message, amount, valid, txhash)]

            # Insert data into the 'transactions' table
            insert_transactions_sql = """
            INSERT INTO transactions (user, type, logdatetime, "from", "to", message, amount, valid, txhash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            cursor.executemany(insert_transactions_sql, transactions_data)

            conn.commit()

            print("Committed to Transaction Table!")

            new_address_2 = '"' + address_2 + '"' #UPDATE HERE

            # Increase if the reciever is the main account

            if (to_var == new_address_2) and (from_var != to_var):

                # Update User Account Balance
                # Define the amount to increase the balance by
                amount_to_increase = amount
                tag_to_update = user

                # Update the balance for tag = 1
                update_query = """
                UPDATE users
                SET balance = balance + ?
                WHERE tag = ?;
                """

                # Execute the update query
                cursor.execute(update_query, (amount_to_increase, tag_to_update))

                conn.commit()
                conn.close()
                print("********** Updated User Table **********")

            # Decrease if the sender is the main account

            elif (from_var == new_address_2) and (from_var != to_var):

                # Update User Account Balance
                # Define the amount to increase the balance by
                amount_to_increase = amount
                tag_to_update = user

                # Update the balance for tag = 1
                update_query = """
                UPDATE users
                SET balance = balance - ?
                WHERE tag = ?;
                """
                # Execute the update query
                cursor.execute(update_query, (amount_to_increase, tag_to_update))

                conn.commit()
                conn.close()
                print("********** Updated User Table **********")
            
        else:
            print("No new transactions found for the specified account address.")
    except Exception as e:
        print(f"An error occurred: {e}")

interval = 60

# Execute a SELECT query to retrieve the Latest_Pole value
cursor.execute("SELECT Latest_Pole FROM query_info")
result = cursor.fetchone()  # Fetch the first row

# Check if the result is None (indicating a NULL value in the database)
if result is None:
    # Calculate the current time in RFC 3339 format
    current_time_rfc3339 = datetime.utcnow().isoformat() + "Z"

    # Calculate the time 60 seconds ago from the current time
    time_60_seconds_ago = datetime.utcnow() - timedelta(seconds=60)

    # Format the time 60 seconds ago in RFC 3339 format
    time_60_seconds_ago_rfc3339 = time_60_seconds_ago.isoformat() + "Z"

    # Insert current time in RFC 3339 into the query_info table
    insert_query_info = f"INSERT INTO query_info (Latest_Pole) VALUES ('{current_time_rfc3339}')"
    cursor.execute(insert_query_info)

else:
    current_time_rfc3339 = result[0]

    # Remove the "+00:00Z" part to make it a valid ISO 8601 format
    current_time_rfc3339 = current_time_rfc3339.replace("+00:00Z", "")

    # Parse the current time into a datetime object
    current_time_dt = datetime.fromisoformat(current_time_rfc3339)

    # Calculate 60 seconds ago
    seconds_ago = timedelta(seconds=60)
    time_60_seconds_ago = current_time_dt - seconds_ago

    # Format the result in RFC3339 format
    time_60_seconds_ago_rfc3339 = time_60_seconds_ago.isoformat() + "Z"
    time_60_seconds_ago_rfc3339 = time_60_seconds_ago_rfc3339.replace("+00:00Z", "Z")

while True:
    # Call the function you want to run
    query(time_60_seconds_ago_rfc3339, current_time_rfc3339)

    # Remove the "+00:00Z" part to make it a valid ISO 8601 format
    current_time_rfc3339 = current_time_rfc3339.replace("+00:00Z", "")
    time_60_seconds_ago_rfc3339 = time_60_seconds_ago_rfc3339.replace("+00:00Z", "")

    # Update each time by a minute
    current_time = datetime.fromisoformat(current_time_rfc3339)
    previous_time = datetime.fromisoformat(time_60_seconds_ago_rfc3339)

    # Calculate 60 seconds ago
    seconds = timedelta(seconds=60)
    time_60_seconds = current_time + seconds
    previous_time_60_seconds = previous_time + seconds

    # Format the result in RFC3339 format
    current_time_rfc3339 = time_60_seconds.isoformat() + "Z"
    time_60_seconds_ago_rfc3339 =  previous_time_60_seconds.isoformat() + "Z"
    time_60_seconds_ago_rfc3339 = time_60_seconds_ago_rfc3339.replace("+00:00Z", "Z")
    current_time_rfc3339 = current_time_rfc3339.replace("+00:00Z", "Z")

    # Wait for the specified interval before running the code again
    time.sleep(interval)
from fastapi import FastAPI, HTTPException

app = FastAPI()

import json
import base64
from dotenv import load_dotenv
import os
import time
from datetime import datetime, timedelta
from algosdk.v2client import indexer
import psycopg2
from psycopg2 import sql

def connect_to_database():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        database="myDatabase",
        user="admin",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    return conn, cursor

def close_database_connection(conn):
    conn.close()

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
        conn, cursor = connect_to_database()

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
            sql_query = "SELECT * FROM users WHERE tag = %s"

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
            INSERT INTO transactions (user_id, type, logdatetime, "from", "to", message, amount, valid, txhash)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.executemany(insert_transactions_sql, transactions_data)

            conn.commit()

            print("Committed to Transaction Table!")

            # Increase if the reciever is the main account

            new_address_2 = '"' + address_2 + '"' #UPDATE HERE

            if (to_var == new_address_2) and (from_var != to_var): #UPDATE HERE
    
                # Update User Account Balance
                # Define the amount to increase the balance by
                amount_to_increase = amount
                tag_to_update = user

                # Update the balance for tag = 1
                update_query = """
                UPDATE users
                SET balance = balance + %s
                WHERE tag = %s;
                """

                # Execute the update query
                cursor.execute(update_query, (amount_to_increase, tag_to_update))

                conn.commit()
                print("********** Updated User Table **********")
                print("Deposit")

            # Decrease if the sender is the main account

            elif (from_var == new_address_2) and (from_var != to_var): # UPDATE HERE

                # Update User Account Balance
                # Define the amount to decrease the balance by
                amount_to_decrease = amount
                tag_to_update = user

                # Update the balance for tag = 1
                update_query = """
                UPDATE users
                SET balance = balance - %s
                WHERE tag = %s;
                """
                # Execute the update query
                cursor.execute(update_query, (amount_to_decrease, tag_to_update))

                conn.commit()
                print("********** Updated User Table **********")
                print("Withdrawal")
        else:
            print("No new transactions found for the specified account address.")

        close_database_connection(conn)
    except Exception as e:
        print(f"An error occurred: {e}")

interval = 60

@app.get("/")
def read_root():
    while True:
        # Call the function you want to run
        query()

        # Wait for the specified interval before running the code again
        time.sleep(interval)
    return {"Response": "Success"}
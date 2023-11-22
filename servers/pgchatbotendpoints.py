from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

import psycopg2
from psycopg2 import sql
import json
import os

from typing import Dict, Any
from base64 import b64decode

from algosdk import account, mnemonic
from algosdk import transaction
from algosdk.v2client import algod
from algosdk.account import generate_account

from dotenv import load_dotenv

load_dotenv()

private_key_1 = os.getenv("FUNDING_ACCOUNT_PRIVATE_KEY")
address_1 = os.getenv("FUNDING_ACCOUNT_ADDRESS")
mnemonic_1 = os.getenv("FUNDING_ACCOUNT_MNEMONIC")
private_key_2 = os.getenv("TEST_ACCOUNT_PRIVATE_KEY")
address_2 = os.getenv("TEST_ACCOUNT_ADDRESS")
mnemonic_2 = os.getenv("TEST_ACCOUNT_MNEMONIC")

# Create an algod client to testnet
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""

algod_client = algod.AlgodClient(algod_token, algod_address)

# Change here ...................
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

# Change here ...................
def close_database_connection(conn):
    conn.close()

# Function to query the user table and return wallet and balance for a given user_id
def query_user_by_id(user_id):
    conn, cursor = connect_to_database()
    
    # Query the user table for the provided user_id
    cursor.execute("SELECT wallet, balance FROM users WHERE tag = %s", (user_id,))
    result = cursor.fetchone()

    
    close_database_connection(conn)
    return result

# Endpoint to check if a user is available
# Returns the true/false
@app.get("/check_user/{user_id}")
def check_user(user_id: int):
    # Call the function to query the user table
    user_data = query_user_by_id(user_id)
    
    if user_data:
        status = True
    else:
        status = False
    return {"status": {status}}

# Endpoint to check balance
# Returns the balance.
@app.get("/check_balance/{user_id}")
def check_balance(user_id: int):
    user_data = query_user_by_id(user_id)
    wallet, balance = user_data
    return {"balance": {balance}}

class WithdrawFundsRequest(BaseModel):
    user_id: int
    reciever_address: str
    amount: int

@app.post("/withdraw_funds")
def withdraw_funds(request: WithdrawFundsRequest):
    user_id = str(request.user_id)
    reciever_address = request.reciever_address
    amount = request.amount

    # Transaction 
    params = algod_client.suggested_params()
    unsigned_txn = transaction.PaymentTxn(
        sender=address_2,
        sp=params,
        receiver=reciever_address,
        amt=amount,
        note=user_id.encode('utf-8'), 
    )

    # sign the transaction
    signed_txn = unsigned_txn.sign(private_key_2)

    # submit the transaction and get back a transaction id
    txid = algod_client.send_transaction(signed_txn)
    print("Successfully submitted transaction with txID: {}".format(txid))

    # wait for confirmation
    txn_result = transaction.wait_for_confirmation(algod_client, txid, 4)

    print(f"Transaction information: {json.dumps(txn_result, indent=4)}")

    # Decode and display the note information of the transaction
    print(f"Decoded note: {b64decode(txn_result['txn']['txn']['note'])}")

    # Return a success message or error message
    return {"results": {txn_result}}

# Endpoint to send money
class MoneyTransferRequest(BaseModel):
    user_id: int
    receiver_id: int
    amount: int

@app.post("/send_money")
async def send_money(request: MoneyTransferRequest):
    user_id = str(request.user_id)
    receiver_id = request.receiver_id
    amount = request.amount

    conn, cursor = connect_to_database()

    # Transaction 
    params = algod_client.suggested_params()
    unsigned_txn = transaction.PaymentTxn(
        sender=address_2,
        sp=params,
        receiver=address_2,
        amt=amount,
        note=user_id.encode('utf-8'),
    )

    # sign the transaction
    signed_txn = unsigned_txn.sign(private_key_2)

    # submit the transaction and get back a transaction id
    txid = algod_client.send_transaction(signed_txn)
    print("Successfully submitted transaction with txID: {}".format(txid))

    # wait for confirmation
    txn_result = transaction.wait_for_confirmation(algod_client, txid, 4)

    print(f"Transaction information: {json.dumps(txn_result, indent=4)}")

    # Decode and display the note information of the transaction
    print(f"Decoded note: {b64decode(txn_result['txn']['txn']['note'])}")

    # Increase Reciever
    # Update the balance for tag = receiver_id
    update_receiver_query = """
    UPDATE users
    SET balance = balance + %s
    WHERE tag = %s;
    """

    # Execute the update query for the receiver
    cursor.execute(update_receiver_query, (amount, receiver_id))

    # Decrease Sender
    # Update the balance for tag = user_id
    update_sender_query = """
    UPDATE users
    SET balance = balance - %s
    WHERE tag = %s;
    """

    # Execute the update query for the sender
    cursor.execute(update_sender_query, (amount, user_id))


    conn.commit()

    close_database_connection(conn)
    print("********** Updated User Table **********")
    # Return a success message or error message
    return {"message": "Money sent successfully"}  # Modify this as needed


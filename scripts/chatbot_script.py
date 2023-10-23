import sqlite3
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

# Function to query the user table and return wallet and balance for a given user_id
def query_user_by_id(user_id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    
    # Query the user table for the provided user_id
    cursor.execute("SELECT wallet, balance FROM users WHERE tag = ?", (user_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    return result

def main(user_id, wallet, balance):
    print(f"Hello user {user_id}. Your balance is {balance} Algos. What would you like to do?")
    
    def check_balance(user_id):
        print("You selected: Balance")
        user_data = query_user_by_id(user_id)
        wallet, balance = user_data
        print(f"Your account balance is {balance} Algos.")

    def withdraw_funds(user_id):
        print("You selected: Withdraw")
        # Add your code to handle withdrawals here
        reciever_address = input("Enter the Algorand Address of the reciever: ")
        amount = int(input("Enter the amount you wish to withdraw: "))
        user_id = str(user_id)

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


    def send_money(user_id):
        print("You selected: Send")
        reciever_id = input("Enter the ID of the reciever: ")
        amount = int(input("Enter the amount you wish to send: "))
        user_id = str(user_id)

        # Connect to the database
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()

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
        # Update the balance for tag = 1
        update_query = """
        UPDATE users
        SET balance = balance + ?
        WHERE tag = ?;
        """

        # Execute the update query
        cursor.execute(update_query, (amount, reciever_id))

        conn.commit()

        # Decrease Sender
        # Update the balance for tag = 1
        update_query = """
        UPDATE users
        SET balance = balance - ?
        WHERE tag = ?;
        """

        # Execute the update query
        cursor.execute(update_query, (amount, user_id))

        conn.commit()

        conn.close()
        print("********** Updated User Table **********")

    while True:
        print("Options:")
        print("1: Balance")
        print("2: Withdraw")
        print("3: Send")
        print("4: Exit")

        choice = input("Enter your choice: ")

        match choice:
            case '1':
                check_balance(user_id)
            case '2':
                withdraw_funds(user_id)
            case '3':
                send_money(user_id)
            case '4':
                print("Exiting the program.")
                break
            case _:
                print("Invalid choice. Please select a valid option.")
    return None


# Main program
print("Welcome to the Farming ChatBot!")

exit_program = False

while True:

    # Get user_id from the user
    user_id = int(input("Enter your user ID: "))

    # Call the function to query the user table
    user_data = query_user_by_id(user_id)

    if user_data:
        print("User found!")
        wallet, balance = user_data
        print(f"Wallet: {wallet}")
        print(f"Balance: {balance}")
        break
    else:
        print("User not found.")
        choice = input("Would you like to try again (yes/no): ").lower()
        if choice == "yes" or choice == "y":
            pass
        else:
            exit_program = True
            break

# Switch Statement for actions
if exit_program:
    pass
else:
    main(user_id, wallet, balance)
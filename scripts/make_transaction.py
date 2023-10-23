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

# Display the balance of the Funding/Transaction account
account_info: Dict[str, Any] = algod_client.account_info(address_1)
print(f"Account balance: {account_info.get('amount')} microAlgos")

# Transaction 
params = algod_client.suggested_params()
unsigned_txn = transaction.PaymentTxn(
    sender=address_1,
    sp=params,
    receiver=address_2,
    amt=1000000,
    note=b"54321",
)

# sign the transaction
signed_txn = unsigned_txn.sign(private_key_1)

# submit the transaction and get back a transaction id
txid = algod_client.send_transaction(signed_txn)
print("Successfully submitted transaction with txID: {}".format(txid))

# wait for confirmation
txn_result = transaction.wait_for_confirmation(algod_client, txid, 4)

print(f"Transaction information: {json.dumps(txn_result, indent=4)}")

# Decode and display the note information of the transaction
print(f"Decoded note: {b64decode(txn_result['txn']['txn']['note'])}")

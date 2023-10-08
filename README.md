# Algorand Transaction Handler

## Overview

This Python-based project facilitates Algorand transaction management on the TestNet. It consists of:

1. **Account Setup**: Create two Algorand accounts (Sender and Receiver) via the Pera Algo Wallet and fund them from a faucet.

2. **Transaction Creator (`make_transaction.py`)**: Send AGLOS from Sender to Receiver with a note using a Python script.

3. **Transaction Query (`transaction_query.py`)**: Continuously monitor the Receiver's address for new transactions and update a SQLite database with transaction details.

4. **Database Schema**: Provides an outline of the database structure for storing transaction information.

## Usage

### 1. Account Setup

- Create and fund the Sender and Receiver accounts securely using the Pera Algo Wallet.

### 2. Transaction Creator (`make_transaction.py`)

To create and send a transaction, run:

```bash
python3 make_transaction.py
```

### 3. Transaction Query (`transaction_query.py`)

Continuously monitor the Receiver's address for new transactions:

```bash
python3 transaction_query.py
```

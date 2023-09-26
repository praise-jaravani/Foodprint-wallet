import sqlite3

# Connect to the database
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Define the SQL query to retrieve data for tag = 1
query = """
SELECT wallet, balance
FROM users
WHERE tag = 1;
"""

# Execute the query
cursor.execute(query)

# Fetch and print the data
result = cursor.fetchone()
if result:
    wallet, balance = result
    print(f"Wallet: {wallet}")
    print(f"Balance: {balance:.6f}")
else:
    print("No data found for tag = 1")

# Close the connection to the database
conn.close()

import sqlite3
from datetime import datetime, timedelta

def insert_user_data(connection, phone, tag, wallet, balance, created, updated=None, country=None):
    try:
        cursor = connection.cursor()

        # Define the SQL statement for inserting data into the "users" table
        insert_query = """
        INSERT INTO users (phone, tag, wallet, balance, created, country)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        # Execute the SQL statement with the provided parameters
        cursor.execute(insert_query, (phone, tag, wallet, balance, created, country))
        connection.commit()

        print(f"User data for {phone} inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Connect to the SQLite database
conn = sqlite3.connect('my_database.db')

# Get the current date and time
current_datetime = datetime.now()

# Format it as 'YYYY-MM-DD HH:MM:SS'
formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

# Example user data as input parameters
user_data = [{"phone": "1234567891", "tag": "54321", "wallet": "rick_wallet", "balance": 1000.000000, "created": formatted_datetime, "country": "SA"}]

# Insert each user's data into the table
for user in user_data:
    insert_user_data(conn, **user)

# Close the connection to the database
conn.close()

# No updated field. Figure out 6 value, 7 column error at some point?

import psycopg2
from psycopg2 import sql
from datetime import datetime

def insert_user_data(connection, phone, tag, wallet, balance, created, updated=None, country=None):
    try:
        cursor = connection.cursor()

        # Define the SQL statement for inserting data into the "users" table
        insert_query = """
        INSERT INTO users (phone, tag, wallet, balance, created, updated, country)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        # Execute the SQL statement with the provided parameters
        cursor.execute(insert_query, (phone, tag, wallet, balance, created, updated, country))
        connection.commit()

        print(f"User data for {phone} inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    database="myDatabase",
    user="admin",
    host="localhost",
    port="5432"
)

# Get the current date and time
current_datetime = datetime.now()

# Format it as 'YYYY-MM-DD HH:MM:SS'
formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

# Example user data as input parameters
user_data = [{"phone": "123456789", "tag": "00000", "wallet": "suspense_wallet", "balance": 0.000000, "created": formatted_datetime, "country": "SA"}]

# Insert each user's data into the table
for user in user_data:
    insert_user_data(conn, **user)

# Close the connection to the database
conn.close()

print("Done!")

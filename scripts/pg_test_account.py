import psycopg2
from urllib.parse import urlparse
from datetime import datetime

# Database URL from Heroku
database_url = "postgres://uvjgyngxorrtjl:b0543e8c6c49823487414b02fe324af2416cb60d54e4bf3cb0e462e80b888ad4@ec2-107-21-67-46.compute-1.amazonaws.com:5432/d2f44igcakhar7"

# Parse the database URL
url = urlparse(database_url)

# Create a connection to the database
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

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

# Get the current date and time
current_datetime = datetime.now()

# Format it as 'YYYY-MM-DD HH:MM:SS'
formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

# Example user data as input parameters
user_data = [{"phone": "123456789", "tag": "12345", "wallet": "suspense_wallet", "balance": 100000.000000, "created": formatted_datetime, "country": "SA"},{"phone": "987654321", "tag": "54321", "wallet": "suspense_wallet", "balance": 100000.000000, "created": formatted_datetime, "country": "SA"} ]

# Insert each user's data into the table
for user in user_data:
    insert_user_data(conn, **user)

# Close the connection to the database
conn.close()

print("Done!")

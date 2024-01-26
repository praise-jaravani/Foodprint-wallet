import psycopg2
from urllib.parse import urlparse

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

# Function to fetch and print user data from the "users" table
def fetch_and_print_user_data(connection):
    try:
        cursor = connection.cursor()

        # Define the SQL statement for selecting data from the "users" table
        select_query = "SELECT * FROM users"

        # Execute the SQL statement
        cursor.execute(select_query)

        # Fetch all the rows and print the results
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except Exception as e:
        print(f"An error occurred while fetching user data: {e}")

# Fetch and print user data from the "users" table
fetch_and_print_user_data(conn)

# Close the connection to the database
conn.close()

print("Done!")

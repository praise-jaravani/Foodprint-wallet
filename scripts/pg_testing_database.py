import psycopg2

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

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    database="myDatabase",
    user="admin",
    host="localhost",
    port="5432"
)

# Fetch and print user data from the "users" table
fetch_and_print_user_data(conn)

# Close the connection to the database
conn.close()

print("Done!")

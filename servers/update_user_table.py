import psycopg2

# Create a connection to the database
conn = psycopg2.connect(
        database="myDatabase",
        user="admin",
        host="localhost",
        port="5432"
    )

cursor = conn.cursor()

# Define the SQL statement for updating the 'users' table
update_users_table = """
ALTER TABLE users
DROP COLUMN IF EXISTS wallet,
DROP COLUMN IF EXISTS country;
"""

cursor.execute(update_users_table)

# Commit the changes and close the connection to the database
conn.commit()
conn.close()

print("Done! Removed wallet and country fields!")

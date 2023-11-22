import psycopg2
from psycopg2 import sql

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    database="myDatabase",
    user="admin",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Define the SQL statements for creating the 'transactions' table
create_transactions_table = """
CREATE TABLE transactions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER,
  type TEXT NOT NULL DEFAULT 'TRANSFER',
  logdatetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "from" TEXT NOT NULL DEFAULT '',
  "to" TEXT NOT NULL DEFAULT '',
  message TEXT DEFAULT NULL,
  amount DECIMAL(20, 6) DEFAULT NULL,
  valid INTEGER NOT NULL DEFAULT 0,
  txhash TEXT NOT NULL DEFAULT ''
);
"""

cursor.execute(create_transactions_table)

# Define the SQL statements for creating the 'users' table
create_users_table = """
CREATE TABLE users (
  phone TEXT NOT NULL DEFAULT '',
  tag SERIAL PRIMARY KEY,
  wallet TEXT NOT NULL DEFAULT '',
  balance NUMERIC(20, 6) NOT NULL DEFAULT 0.000000,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated TIMESTAMP NULL DEFAULT NULL,
  country TEXT DEFAULT NULL
);
"""

cursor.execute(create_users_table)

# Define the SQL statement for creating the 'query_info' table
create_query_info_table = """
CREATE TABLE query_info (
  Latest_Pole TEXT DEFAULT NULL
);
"""

cursor.execute(create_query_info_table)

# Commit the changes and close the connection to the database
conn.commit()
conn.close()

print("Done!")

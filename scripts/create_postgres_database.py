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

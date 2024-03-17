import sqlite3

# Connect to your database
conn = sqlite3.connect('db.sqlite')

# Create a cursor object
cur = conn.cursor()

# Retrieve the schema of your table
cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='user';")

# Fetch and print the result
print(cur.fetchone()[0])

# Close the connection
conn.close()

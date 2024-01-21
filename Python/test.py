import mysql.connector

host = "localhost"
user = "aprioriUser"
password = "aprioripwd"
database = "aprioriBase"

# Connect to MySQL
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Create a cursor
cursor = conn.cursor()

# Check if the cursor is closed
if cursor.closed:
    print("Cursor is closed.")
else:
    print("Cursor is open.")

# Close the cursor
cursor.close()

# Check again after closing
if cursor.closed:
    print("Cursor is closed.")
else:
    print("Cursor is open.")

# Close the connection
conn.close()

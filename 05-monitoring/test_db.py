import psycopg2

# Connect to your postgres DB
conn = psycopg2.connect("host=localhost user=postgres password=example")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM my_data")

# Retrieve query results
records = cur.fetchall()
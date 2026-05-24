# Kokoro Chat Storage Example Output

"/PATH/TO/YOUR/.venv/bin/python" /PROJECT/PATH/kokoro/inference/chat_storage.py

Conversation ID:  1

User: Hi, what is your name? I need help on a python script.

Kokoro:  Hi there! My name is Kokoro, a helpful AI coding assistant. I'm more than happy to help you with your Python script. Can you please describe the issue you're facing or the specific task you need assistance with?

User: How would I append to an SQL database?

Kokoro:  To append data to an SQL database using Python, you'll want to use a library like `sqlite3` or `psycopg2` (for PostgreSQL). Here's a simple example of appending data to an SQLite database using the `sqlite3` module.

First, establish a connection to the database:

```python
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('my_database.db')

# Create a cursor object
cursor = conn.cursor()
```

Then, you'll want to create a new table or use an existing one:

```python
# Create a table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS my_table(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    column1 TEXT,
                    column2 TEXT
                )''')
```

Finally, append data to the database:

```python
# Insert new row
new_data = ('value1', 'value2')
cursor.execute("INSERT INTO my_table (column1, column2) VALUES (?, ?)", new_data)

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()
```

In this example, we're using a SQLite database, but the concept is the same for other SQL-based databases like MySQL or PostgreSQL using the appropriate library (e.g., `pyodbc`, `mysql-connector-python`, or `psycopg2`).


Process finished with exit code 0

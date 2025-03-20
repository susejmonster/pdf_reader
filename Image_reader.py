import sqlite3

# Connect to the SQLite database (change 'my_database.db' to your DB file)
conn = sqlite3.connect("BOM.db")
cursor = conn.cursor()

def run_query(query):
    """Executes a custom SQL query and displays the result."""
    try:
        cursor.execute(query)
        if query.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No results found.")
        else:
            conn.commit()
            print("Query executed successfully.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

# Interactive query input
while True:
    user_query = input("\nEnter your SQL query (or type 'exit' to quit): ").strip()
    if user_query.lower() == "exit":
        break
    run_query(user_query)

# Close the database connection
conn.close()

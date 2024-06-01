
import sqlite3
from datetime import datetime

def create_quotes_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS quotes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT,
                  what_happened TEXT,
                  details TEXT,
                  quote TEXT)''')
    conn.commit()

def insert_quote(conn, what_happened, details):
    quote = f"# {what_happened} - {details}"
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c = conn.cursor()
    c.execute("INSERT INTO quotes (date, what_happened, details, quote) VALUES (?, ?, ?, ?)", (date, what_happened, details, quote))
    conn.commit()

def retrieve_quotes(conn):
    c = conn.cursor()
    current_date = datetime.now().strftime('%Y-%m-%d')
    c.execute("SELECT what_happened, details, quote FROM quotes WHERE date LIKE ?", (f"{current_date}%",))
    return c.fetchall()

def delete_today_quotes(conn):
    c = conn.cursor()
    current_date = datetime.now().strftime('%Y-%m-%d')
    c.execute("DELETE FROM quotes WHERE date LIKE ?", (f"{current_date}%",))
    conn.commit()
    print("Today's quotes deleted.")


import os
import keyboard
import sqlite3
from app.controller.controller import handle_add_quote, handle_delete_quotes
from app.queries.queries import create_quotes_table

def main():
    print("\nAdd new stories: Ctrl + K\nDelete today's stories: Ctrl + J")

    if not os.path.exists('quotes.db'):
        conn = sqlite3.connect('quotes.db')
        create_quotes_table(conn)
        conn.close()

    keyboard.add_hotkey('ctrl+k', handle_add_quote)
    keyboard.add_hotkey('ctrl+j', handle_delete_quotes)

    print("Press Ctrl + C to quit.\n")
    try:
        keyboard.wait('ctrl+c')
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()

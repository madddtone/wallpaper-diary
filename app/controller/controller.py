
import os
import sqlite3
import easygui as eg
import win32gui
import win32con
from datetime import datetime

from app.queries.queries import create_quotes_table, insert_quote, retrieve_quotes, delete_today_quotes
from app.image_generator.image_process import create_image_with_quotes, set_desktop_background

def handle_add_quote():
    conn = sqlite3.connect('quotes.db')
    create_quotes_table(conn)

    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)

    what_happened = eg.enterbox("What happened?", "Wallpaper Diary by Khalil Azmi")
    if what_happened is None:
        conn.close()
        return

    details = eg.enterbox("Details?", "Wallpaper Diary by Khalil Azmi")
    if details is None:
        conn.close()
        return

    insert_quote(conn, what_happened, details)
    quotes = retrieve_quotes(conn)

    output_dir = "C:\\diary"
    os.makedirs(output_dir, exist_ok=True)
    current_date = datetime.now().strftime('%d-%m-%Y')
    image_filename = os.path.join(output_dir, f"{current_date}.png")
    display_quotes = [f"#{i+1} {quote[0]} - {quote[1]}" for i, quote in enumerate(quotes)]

    image_path = create_image_with_quotes(display_quotes, image_filename)
    print("Image path:", image_path)
    set_desktop_background(image_path)

    conn.close()

def handle_delete_quotes():
    conn = sqlite3.connect('quotes.db')
    create_quotes_table(conn)

    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)

    if eg.ynbox("Are you sure you want to delete today's quotes?", "Confirm Delete"):
        delete_today_quotes(conn)
    else:
        print("Deletion canceled.")

    conn.close()


import os
import sqlite3
import ctypes
from datetime import datetime
import easygui as eg
from PIL import Image, ImageDraw, ImageFont
from screeninfo import get_monitors
import keyboard
import win32gui
import win32con

def create_image_with_quotes(quotes, filename):
    monitor = get_monitors()[0]
    width, height = monitor.width, monitor.height

    max_height = int(height * 0.9)
    img = Image.new('RGB', (width, height), color=(30, 30, 46))
    d = ImageDraw.Draw(img)

    font_size = 20
    try:
        font = ImageFont.truetype("JetBrainsMonoNerdFont-SemiBold.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    padding = 10
    height_column1 = padding
    height_column2 = padding

    for i, quote in enumerate(quotes):
        text_bbox = d.textbbox((0, 0), quote, font=font)
        text_height = text_bbox[3] - text_bbox[1]

        if height_column1 + text_height + padding * 2 <= max_height:
            x_position = padding
            y_position = height_column1
            height_column1 += text_height + padding * 2
        else:
            x_position = width // 2 + padding
            y_position = height_column2
            height_column2 += text_height + padding * 2

        d.text((x_position, y_position), quote, fill=(255, 255, 255), font=font)

    img.save(filename)
    print(f"Image saved as {filename}")
    return filename

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

def set_desktop_background(image_path):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

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

def main():
    print("Add new stories: Ctrl + K\nDelete today's stories: Ctrl + J")

    if not os.path.exists('quotes.db'):
        conn = sqlite3.connect('quotes.db')
        create_quotes_table(conn)
        conn.close()

    keyboard.add_hotkey('ctrl+k', handle_add_quote)
    keyboard.add_hotkey('ctrl+j', handle_delete_quotes)

    print("Press Ctrl + C to quit.")
    try:
        keyboard.wait('ctrl+c')
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()

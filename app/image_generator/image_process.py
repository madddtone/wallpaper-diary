
import os
import ctypes
from PIL import Image, ImageDraw, ImageFont
from screeninfo import get_monitors

def create_image_with_quotes(quotes, filename):
    monitor = get_monitors()[0]
    width, height = monitor.width, monitor.height

    max_height = int(height * 0.9)
    img = Image.new('RGB', (width, height), color=(30, 30, 46))
    d = ImageDraw.Draw(img)

    font_size = 20
    try:
        font = ImageFont.truetype("assets/JetBrainsMonoNerdFont-SemiBold.ttf", font_size)
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

def set_desktop_background(image_path):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

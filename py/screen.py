from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
import time

def display_on_screen(afr, temperature):
    """
    Displays the AFR and temperature on an I2C screen.

    :param afr: Air-Fuel Ratio to display.
    :param temperature: Temperature to display.
    """
    # Initialize I2C and display
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial, width=128, height=64)

    # Create drawing canvas
    width = device.width
    height = device.height
    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Clear display
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Load and draw cat image
    message = f"AFR: {afr} Temp: {temperature}"
    draw.text((0, 0), message, font=font, fill=255)
    
    # Draw a cat
    cat = Image.open("cats/nyan-sit.png").convert("1")
    original_size = cat.size
    print(f"Original cat size: {original_size}")
    new_size = (50 , 36)
    
    resized_cat = cat.resize(new_size, Image.BICUBIC)
    
    image.paste(resized_cat, (0, 16))    
    
    device.display(image)
    time.sleep(2)

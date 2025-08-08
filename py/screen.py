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

    # Display text
    message = f"AFR: {afr} Temp: {temperature}"
    draw.text((0, 0), message, font=font, fill=255)
    
    # draw.image 
    
    device.display(image)
    time.sleep(2)

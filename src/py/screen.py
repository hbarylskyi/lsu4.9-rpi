from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

# --- Initialize once ---
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)
width = device.width
height = device.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

def display_on_screen(afr, temperature):
    """
    Fast display update: updates AFR and temperature without recreating objects.
    """
    # Clear previous content
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Draw new text
    message = f"AFR: {afr}  Temp: {temperature}"
    draw.text((0, 0), message, font=font, fill=255)

    # Push to display
    device.display(image)
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
import time

# Initialize I2C and display
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

# Create drawing canvas
width = device.width
height = device.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Turn on all pixels
draw.rectangle((0, 0, width, height), outline=255, fill=255)
device.display(image)
time.sleep(0.5)

# Turn off all pixels
draw.rectangle((0, 0, width, height), outline=0, fill=0)
device.display(image)
time.sleep(0.5)

# Set individual pixels
draw.point((0, 0), fill=255)
draw.point((64, 0), fill=255)
draw.point((127, 63), fill=255)
device.display(image)
time.sleep(0.3)

# Clear again
draw.rectangle((0, 0, width, height), outline=0, fill=0)
device.display(image)
time.sleep(0.1)

# Display text
draw.text((0, 0), "Hello, motherfucker!", font=font, fill=255)
draw.text((20, 50), "freak", font=font, fill=255)
device.display(image)
time.sleep(2)
draw.rectangle((0, 0, width, height), outline=0, fill=0)

draw.text((3, 3), "who killed john kennedy", font=font, fill=255)
draw.text((30, 30), "...", font=font, fill=100)
device.display(image)
time.sleep(5)

# Final clear
draw.rectangle((0, 0, width, height), outline=0, fill=0)
device.display(image)


from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
import os

# Load a font with a specific size
font_size = 22  # adjust as needed
font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", font_size)

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)
width = device.width
height = device.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

script_dir = os.path.dirname(__file__)
cat_path = os.path.join(script_dir, "cats", "0cat-white.png")
cat_image = Image.open(cat_path).convert("1")
resized_cat = cat_image.resize((75, 54), Image.NEAREST) 

def display_on_screen(afr, temperature):
    """
    Fast display update: updates AFR and temperature without recreating objects.
    """
    # Clear previous content
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # # Draw new text
    # message = f"AFR: {afr}  Temp: {temperature}"
    # draw.text((0, 0), message, font=font, fill=255)
    # image.paste(resized_cat, (width - 75, 10))

    # # Push to display
    # device.display(image)
    
    image.paste(resized_cat, (width - 75, 16))  # adjust vertical as needed

    # Draw AFR and Temp below the cat
    text_y = 54  # start below cat height
    message = f"Temp: {temperature}"
    draw.text((0, 0), message, font=font, fill=255)
    draw.text((0, 16), f"{afr}", font=font_large, fill=255)

    # Update display
    device.display(image)
import time
import os
from PIL import Image
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

# Initialize I2C and display
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

# Load animation frames from "frames/" folder
def load_frames(folder):
    frames = []
    for file in sorted(os.listdir(folder)):
        if file.lower().endswith((".png", ".bmp")):
            path = os.path.join(folder, file)
            image = Image.open(path).convert("1").resize((device.width, device.height))
            frames.append(image)
    return frames

frames = load_frames("cats")

if not frames:
    raise RuntimeError("No frames found in ./cats/")
device.display(frames[0])  # Display the first frame
time.sleep(10.05)  # adjust speed
# Loop animation
# while True:
#     device.display(frames[0])  # Display the first frame
#     time.sleep(0.05)  # adjust speed
    # for frame in frames:
        


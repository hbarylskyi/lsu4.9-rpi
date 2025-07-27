import smbus
import time

# Constants for the SSD1306
SSD1306_I2C_ADDRESS = 0x3C
SSD1306_COMMAND = 0x00
SSD1306_DISPLAY_ON = 0xAF
SSD1306_DISPLAY_OFF = 0xAE

class SSD1306:
    def __init__(self, i2c_bus=1):
        self.bus = smbus.SMBus(i2c_bus)

    def send_command(self, command):
        self.bus.write_byte_data(SSD1306_I2C_ADDRESS, SSD1306_COMMAND, command)

    def turn_on(self):
        self.send_command(SSD1306_DISPLAY_ON)

    def turn_off(self):
        self.send_command(SSD1306_DISPLAY_OFF)

if __name__ == "__main__":
    display = SSD1306()
    display.turn_on()
    time.sleep(2)
    display.turn_off()

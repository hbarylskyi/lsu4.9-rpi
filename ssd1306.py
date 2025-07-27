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

    def initialize(self):
        # Initialization sequence for SSD1306
        init_sequence = [
            0xAE,  # Display off
            0xD5, 0x80,  # Set display clock divide ratio/oscillator frequency
            0xA8, 0x3F,  # Set multiplex ratio (1 to 64)
            0xD3, 0x00,  # Set display offset
            0x40,  # Set start line address
            0x8D, 0x14,  # Charge pump setting
            0x20, 0x00,  # Memory addressing mode
            0xA1,  # Set segment re-map
            0xC8,  # Set COM output scan direction
            0xDA, 0x12,  # Set COM pins hardware configuration
            0x81, 0xCF,  # Set contrast control
            0xD9, 0xF1,  # Set pre-charge period
            0xDB, 0x40,  # Set VCOMH deselect level
            0xA4,  # Entire display on
            0xA6,  # Set normal display
            0xAF  # Display on
        ]
        for cmd in init_sequence:
            self.send_command(cmd)

    def turn_on(self):
        self.initialize()
        self.send_command(SSD1306_DISPLAY_ON)

    def test_pattern(self):
        # Fill the screen with a test pattern
        for i in range(0, 128 * 8):
            self.bus.write_byte_data(SSD1306_I2C_ADDRESS, 0x40, 0xFF)  # 0x40 is the data mode

    def turn_off(self):
        self.send_command(SSD1306_DISPLAY_OFF)

if __name__ == "__main__":
    display = SSD1306()
    display.turn_on()
    display.test_pattern()
    time.sleep(5)
    display.turn_off()

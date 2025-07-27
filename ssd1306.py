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
            0xA0,  # Set segment re-map
            0xC8,  # Set COM output scan direction
            0xDA, 0x12,  # Set COM pins hardware configuration
            0x81, 0x7F,  # Set contrast control
            0xD9, 0xF1,  # Set pre-charge period
            0xDB, 0x40,  # Set VCOMH deselect level
            0xA4,  # Entire display on
            0xA6,  # Set normal display
            0xAF,  # Display on
            
        ]
        for cmd in init_sequence:
            self.send_command(cmd)

    def turn_on(self):
        self.initialize()
        self.send_command(SSD1306_DISPLAY_ON)

    def clear_display(self):
        # Clear the display by filling it with zeros
        self.ssd1306_fillscreen(0x00)

    def ssd1306_fillscreen(self, fill):
        self.set_position(0, 0)
        for i in range(0, 128 * 8):
            self.bus.write_byte_data(SSD1306_I2C_ADDRESS, 0x40, fill)

    def display_text(self, text, x=0, y=0):
        # Clear the display before writing new text
        self.clear_display()
        # Set position to start displaying text
        self.set_position(x, y)
        for char in text:
            # self.write_char(char)
            # self.bus.write_i2c_block_data(SSD1306_I2C_ADDRESS, 0x40, 0x3E)
            self.bus.write_byte_data(SSD1306_I2C_ADDRESS, 0x40, ord(char))
            self.set_position(x+ 20, y + 5 + 1)  # Move cursor to the right for next character

    def write_char(self, char):
        c = char - 32
        
        
 
    #     for (i= 0; i < 6; i++)
	# {
	# 	ssd1306_send_byte(pgm_read_byte(&ssd1306xled_font6x8[c * 6 + i]));
	# }
        
        # self.bus.write_i2c_block_data(SSD1306_I2C_ADDRESS, 0x40, char)
        # for i in range(5):
        #     self.bus.write_byte_data(SSD1306_I2C_ADDRESS, 0x40, font_data[i])    
        self.bus.write_byte_data(SSD1306_I2C_ADDRESS, 0x40, char)  # Space between characters

    def set_position(self, x, y):
        self.send_command(0xB0 + y)
        self.send_command(0x00 + (x & 0x0F))
        self.send_command(0x10 + ((x >> 4) & 0x0F))

    def display_image(self, image):
        # Display a bitmap image
        self.set_position(0, 0)
        for byte in image:
            self.bus.write_byte_data(SSD1306_I2C_ADDRESS, 0x40, byte)
        # Fill the screen with a test pattern
        for i in range(0, 128 * 8):
            self.bus.write_byte_data(SSD1306_I2C_ADDRESS, 0x40, 0xFF)  # 0x40 is the data mode

    def turn_off(self):
        self.send_command(SSD1306_DISPLAY_OFF)

if __name__ == "__main__":
    display = SSD1306()
    display.initialize()
    display.display_text("Hello, World!", 0, 10)
    # Example cat image (replace with actual image data)
    # cat_image = [
    #     0x00, 0x3C, 0x42, 0xA9, 0x85, 0xA9, 0x91, 0x42, 0x3C, 0x00,
    #     # Add more bytes to complete the image
    # ]
    # display.display_image(cat_image)
    time.sleep(10)
    display.turn_off()

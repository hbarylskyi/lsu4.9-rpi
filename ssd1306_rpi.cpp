#include <iostream>
#include <cstdint>
#include <unistd.h> // For usleep
#include <pigpio.h>

#define SSD1306_I2C_ADDRESS 0x3C


const uint8_t ssd1306_init_sequence []  = {	// Initialization Sequence
	0xAE,			// Set Display ON/OFF - AE=OFF, AF=ON
	0xD5, 0xF0,		// Set display clock divide ratio/oscillator frequency, set divide ratio
	0xA8, 0x3F,		// Set multiplex ratio (1 to 64) ... (height - 1)
	0xD3, 0x00,		// Set display offset. 00 = no offset
	0x40 | 0x00,	// Set start line address, at 0.
	0x8D, 0x14,		// Charge Pump Setting, 14h = Enable Charge Pump
	0x20, 0x00,		// Set Memory Addressing Mode - 00=Horizontal, 01=Vertical, 10=Page, 11=Invalid
	0xA0 | 0x01,	// Set Segment Re-map
	0xC8,			// Set COM Output Scan Direction
	0xDA, 0x12,		// Set COM Pins Hardware Configuration - 128x32:0x02, 128x64:0x12
	0x81, 0x3F,		// Set contrast control register
	0xD9, 0x22,		// Set pre-charge period (0x22 or 0xF1)
	0xDB, 0x20,		// Set Vcomh Deselect Level - 0x00: 0.65 x VCC, 0x20: 0.77 x VCC (RESET), 0x30: 0.83 x VCC
	0xA4,			// Entire Display ON (resume) - output RAM to display
	0xA6,			// Set Normal/Inverse Display mode. A6=Normal; A7=Inverse
	0x2E,			// Deactivate Scroll command
	0xAF,			// Set Display ON/OFF - AE=OFF, AF=ON
};
class SSD1306Device {
public:
    SSD1306Device();
    void begin();
    void ssd1306_init();
    void ssd1306_fillscreen(uint8_t fill);
    void ssd1306_setpos(uint8_t x, uint8_t y);
    void ssd1306_char_font6x8(char ch);
    void ssd1306_string_font6x8(const char *s);

private:
    int fd;
    void send_command(uint8_t command);
    void send_data(uint8_t data);
};

SSD1306Device::SSD1306Device() {
    if (gpioInitialise() < 0) {
        std::cerr << "Failed to initialize pigpio.\n";
        exit(1);
    }
    fd = i2cOpen(1, SSD1306_I2C_ADDRESS, 0);
    if (fd == -1) {
        std::cerr << "Failed to init I2C communication.\n";
        exit(1);
    }
}

void SSD1306Device::begin() {
    ssd1306_init();
}

void SSD1306Device::send_command(uint8_t command) {
    // i2cWriteByteData(fd, 0x00, command);
}

void SSD1306Device::send_data(uint8_t data) {
    // i2cWriteByteData(fd, 0x40, data);
}

void SSD1306Device::ssd1306_init() {
    const uint8_t init_sequence[] = {
        0xAE,  // Display off
        0xD5, 0xF0,  // Set display clock divide ratio/oscillator frequency
        0xA8, 0x3F,  // Set multiplex ratio (1 to 64)
        0xD3, 0x00,  // Set display offset
        0x40,  // Set start line address
        0x8D, 0x14,  // Charge pump setting
        0x20, 0x00,  // Memory addressing mode
        0xA0,  // Set segment re-map
        0xC8,  // Set COM output scan direction
        0xDA, 0x12,  // Set COM pins hardware configuration
        0x81, 0x3F,  // Set contrast control
        0xD9, 0x22,  // Set pre-charge period
        0xDB, 0x20,  // Set VCOMH deselect level
        0xA4,  // Entire display on
        0xA6,  // Set normal display
        0xAF,  // Display on
    };
    for (uint8_t cmd : init_sequence) {
        send_command(cmd);
    }
    ssd1306_fillscreen(0x00);
}

void SSD1306Device::ssd1306_fillscreen(uint8_t fill) {
    for (uint8_t page = 0; page < 8; ++page) {
        ssd1306_setpos(0, page);
        for (uint8_t col = 0; col < 128; ++col) {
            send_data(fill);
        }
    }
}

void SSD1306Device::ssd1306_setpos(uint8_t x, uint8_t y) {
    send_command(0xB0 | y);
    send_command(0x00 | (x & 0x0F));
    send_command(0x10 | ((x >> 4) & 0x0F));
}

void SSD1306Device::ssd1306_char_font6x8(char ch) {
    // Implement character drawing using a font array
}

void SSD1306Device::ssd1306_string_font6x8(const char *s) {
    while (*s) {
        ssd1306_char_font6x8(*s++);
    }
}

int main() {
    SSD1306Device display;
    display.begin();
    display.ssd1306_fillscreen(0x00);
    display.ssd1306_string_font6x8("Hello, Raspberry Pi!");
    display.ssd1306_string_font6x8("Hello, Raspberry Pi!");
    usleep(5000000); // Keep the message on screen for 5 seconds
    usleep(5000000); // Keep the message on screen for 5 seconds
    display.ssd1306_fillscreen(0x00); // Clear the screen
    // i2cClose(fd);
    gpioTerminate();
    return 0;
}
#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <iostream>
#include <unistd.h>

#define SSD1306_I2C_ADDRESS 0x3C
#define SSD1306_COMMAND 0x00
#define SSD1306_DATA 0x40

class SSD1306Device {
public:
    SSD1306Device();
    void begin();
    void ssd1306_init();
    void ssd1306_fillscreen(uint8_t fill);
    void ssd1306_setpos(uint8_t x, uint8_t y);
    void ssd1306_char_font6x8(char ch);
    void ssd1306_string_font6x8(const char *s);

private:
    int fd;
    void send_command(uint8_t command);
    void send_data(uint8_t data);
};

SSD1306Device::SSD1306Device() {
    fd = wiringPiI2CSetup(SSD1306_I2C_ADDRESS);
    if (fd == -1) {
        std::cerr << "Failed to initialize I2C communication.\n";
        exit(1);
    }
}

void SSD1306Device::begin() {
    ssd1306_init();
}

void SSD1306Device::ssd1306_init() {
    const uint8_t init_sequence[] = {
        0xAE, 0xD5, 0xF0, 0xA8, 0x3F, 0xD3, 0x00, 0x40, 0x8D, 0x14,
        0x20, 0x00, 0xA0, 0xC8, 0xDA, 0x12, 0x81, 0x3F, 0xD9, 0x22,
        0xDB, 0x20, 0xA4, 0xA6, 0x2E, 0xAF
    };
    for (uint8_t cmd : init_sequence) {
        send_command(cmd);
    }
}

void SSD1306Device::send_command(uint8_t command) {
    wiringPiI2CWriteReg8(fd, SSD1306_COMMAND, command);
}

void SSD1306Device::send_data(uint8_t data) {
    wiringPiI2CWriteReg8(fd, SSD1306_DATA, data);
}

void SSD1306Device::ssd1306_fillscreen(uint8_t fill) {
    for (uint8_t page = 0; page < 8; ++page) {
        ssd1306_setpos(0, page);
        for (uint8_t col = 0; col < 128; ++col) {
            send_data(fill);
        }
    }
}

void SSD1306Device::ssd1306_setpos(uint8_t x, uint8_t y) {
    send_command(0xB0 | y);
    send_command(0x00 | (x & 0x0F));
    send_command(0x10 | ((x >> 4) & 0x0F));
}

void SSD1306Device::ssd1306_char_font6x8(char ch) {
    // Implement character drawing using a font array
}

void SSD1306Device::ssd1306_string_font6x8(const char *s) {
    while (*s) {
        ssd1306_char_font6x8(*s++);
    }
}

int main() {
    wiringPiSetup();
    SSD1306Device display;
    display.begin();
    display.ssd1306_fillscreen(0x00);
    display.ssd1306_string_font6x8("Hello, Raspberry Pi!");
    usleep(5000000); // Keep the message on screen for 5 seconds
    display.ssd1306_fillscreen(0x00); // Clear the screen
    return 0;
}

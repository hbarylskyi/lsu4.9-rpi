#include <iostream>
#include <cstdint>
#include <unistd.h> // For usleep
#include <wiringPiI2C.h>

#define SSD1306_I2C_ADDRESS 0x3C

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
        std::cerr << "Failed to init I2C communication.\n";
        exit(1);
    }
}

void SSD1306Device::begin() {
    ssd1306_init();
}

void SSD1306Device::send_command(uint8_t command) {
    wiringPiI2CWriteReg8(fd, 0x00, command);
}

void SSD1306Device::send_data(uint8_t data) {
    wiringPiI2CWriteReg8(fd, 0x40, data);
}

void SSD1306Device::ssd1306_init() {
    const uint8_t init_sequence[] = {
        0xAE, 0xD5, 0x80, 0xA8, 0x3F, 0xD3, 0x00, 0x40, 0x8D, 0x14,
        0x20, 0x00, 0xA1, 0xC8, 0xDA, 0x12, 0x81, 0x7F, 0xD9, 0xF1,
        0xDB, 0x40, 0xA4, 0xA6, 0xAF
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
    usleep(5000000); // Keep the message on screen for 5 seconds
    display.ssd1306_fillscreen(0x00); // Clear the screen
    return 0;
}

#include <iostream>
#include <wiringPiI2C.h>
#include <unistd.h>

#define SSD1306_I2C_ADDRESS 0x3C
#define SSD1306_COMMAND 0x00
#define SSD1306_DATA 0x40

class SSD1306 {
public:
    SSD1306();
    void initialize();
    void sendCommand(uint8_t command);
    void sendData(uint8_t data);
    void displayOn();
    void displayOff();
    void clearDisplay();
    void displayText(const std::string& text);

private:
    int fd;
};

SSD1306::SSD1306() {
    fd = wiringPiI2CSetup(SSD1306_I2C_ADDRESS);
    if (fd == -1) {
        std::cerr << "Failed to initialize I2C communication.\n";
        exit(1);
    }
}

void SSD1306::initialize() {
    sendCommand(0xAE); // Display off
    sendCommand(0xD5); // Set display clock divide ratio/oscillator frequency
    sendCommand(0x80); // Suggested ratio
    sendCommand(0xA8); // Set multiplex ratio
    sendCommand(0x3F);
    sendCommand(0xD3); // Set display offset
    sendCommand(0x00); // No offset
    sendCommand(0x40); // Set start line address
    sendCommand(0x8D); // Charge pump
    sendCommand(0x14);
    sendCommand(0x20); // Memory addressing mode
    sendCommand(0x00); // Horizontal addressing mode
    sendCommand(0xA1); // Set segment re-map
    sendCommand(0xC8); // Set COM output scan direction
    sendCommand(0xDA); // Set COM pins hardware configuration
    sendCommand(0x12);
    sendCommand(0x81); // Set contrast control
    sendCommand(0xCF);
    sendCommand(0xD9); // Set pre-charge period
    sendCommand(0xF1);
    sendCommand(0xDB); // Set Vcomh deselect level
    sendCommand(0x40);
    sendCommand(0xA4); // Entire display on
    sendCommand(0xA6); // Set normal display
    sendCommand(0xAF); // Display on
}

void SSD1306::sendCommand(uint8_t command) {
    wiringPiI2CWriteReg8(fd, SSD1306_COMMAND, command);
}

void SSD1306::sendData(uint8_t data) {
    wiringPiI2CWriteReg8(fd, SSD1306_DATA, data);
}

void SSD1306::displayOn() {
    sendCommand(0xAF);
}

void SSD1306::displayOff() {
    sendCommand(0xAE);
}

void SSD1306::clearDisplay() {
    for (int i = 0; i < 1024; i++) {
        sendData(0x00);
    }
}

void SSD1306::displayText(const std::string& text) {
    for (char c : text) {
        // Implement character to byte mapping here
        sendData(c);
    }
}

int main() {
    SSD1306 display;
    display.initialize();
    display.clearDisplay();
    display.displayText("Hello, Raspberry Pi!");
    return 0;
}

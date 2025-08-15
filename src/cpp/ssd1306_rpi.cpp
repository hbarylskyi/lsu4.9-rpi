#include <iostream>
#include <wiringPiI2C.h>
#include <unistd.h>
#include <iostream>
#include <fcntl.h>
#include <sys/ioctl.h>

#define SSD1306_I2C_ADDRESS 0x3C
#define SSD1306_COMMAND 0x00
#define SSD1306_DATA 0x40

const uint8_t ssd1306_init_sequence [] = {	// Initialization Sequence
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
class SSD1306 {
public:
    SSD1306();
    void initialize();
    void sendCommand(uint8_t command);
    void ssd1306_send_command(uint8_t cmd);
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
	// begin();

	// sendCommand(0x00);

    uint8_t init_sequence[] = {
        0xAE, 0xD5, 0xF0, 0xA8, 0x3F, 0xD3, 0x00,
        0x40 | 0x00, 0x8D, 0x14, 0x20, 0x00,
        0xA0 | 0x01, 0xC8, 0xDA, 0x12, 0x81, 0x3F,
        0xD9, 0x22, 0xDB, 0x20, 0xA4, 0xA6,
        0x2E, 0xAF
    };

    for (uint8_t i = 0; i < sizeof(init_sequence); i++) {
        SSD1306::sendCommand(init_sequence[i]);
        usleep(1000);  // Short delay for safety
    }

	// for (uint8_t i = 0; i < sizeof (ssd1306_init_sequence); i++) {
	// 	ssd1306_send_byte(pgm_read_byte(&ssd1306_init_sequence[i]));
	// }
	// ssd1306_send_command_stop();
	// ssd1306_fillscreen(0);

    // ssd1306_init();
    // sendCommand(0xAE); // Display off
    // sendCommand(0xD5); // Set display clock divide ratio/oscillator frequency
    // sendCommand(0x80); // Suggested ratio
    // sendCommand(0xA8); // Set multiplex ratio
    // sendCommand(0x3F);
    // sendCommand(0xD3); // Set display offset
    // sendCommand(0x00); // No offset
    // sendCommand(0x40); // Set start line address
    // sendCommand(0x8D); // Charge pump
    // sendCommand(0x14);
    // sendCommand(0x20); // Memory addressing mode
    // sendCommand(0x00); // Horizontal addressing mode
    // sendCommand(0xA1); // Set segment re-map
    // sendCommand(0xC8); // Set COM output scan direction
    // sendCommand(0xDA); // Set COM pins hardware configuration
    // sendCommand(0x12);
    // sendCommand(0x81); // Set contrast control
    // sendCommand(0xCF);
    // sendCommand(0xD9); // Set pre-charge period
    // sendCommand(0xF1);
    // sendCommand(0xDB); // Set Vcomh deselect level
    // sendCommand(0x40);
    // sendCommand(0xA4); // Entire display on
    // sendCommand(0xA6); // Set normal display
    // sendCommand(0xAF); // Display on
}

// void SSD1306::begin() {
// 	I2CInit();
// #ifndef TINY4KOLED_QUICK_BEGIN
// 	while (!I2CStart(SSD1306_SA, 0)) {
// 		delay(10);
// 	}
// 	I2CStop();
// #endif
// }


// void ssd1306_send_command(uint8_t cmd) {
//     uint8_t buffer[2] = {0x00, cmd};  // 0x00 = command mode
//     write(i2c_fd, buffer, 2);
// }

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
        // Simple ASCII to byte mapping for demonstration
        // This should be replaced with actual font data
        uint8_t byte = static_cast<uint8_t>(c);
        sendData(byte);
    }
}

int main() {
    SSD1306 display = SSD1306();
    display.initialize();
    
    display.clearDisplay();
    display.displayText("Hello, Raspberry Pi!");
    return 0;
}

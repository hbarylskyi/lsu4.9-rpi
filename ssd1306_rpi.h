#ifndef SSD1306_RPI_H
#define SSD1306_RPI_H

#include <string>

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

#endif // SSD1306_RPI_H

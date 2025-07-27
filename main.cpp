
#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <iostream>
#include <string>

int main() {
    SSD1306 display;
    display.ssd1306_init();
    display.clearDisplay();
    display.displayText("Hello, Raspberry Pi!");
    return 0;
}

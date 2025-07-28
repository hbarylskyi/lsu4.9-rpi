
#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <iostream>
#include <string>
#include "ssd1306_rpi.h"

int main() {
    SSD1306 display = SSD1306();
    display.initialize();
    
    display.clearDisplay();
    display.displayText("Hello, Raspberry Pi!");
    return 0;
}

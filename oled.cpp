#include "ssd1306/ssd1306xled.h"

void setup() {
    //_delay_ms(40);
    SSD1306.ssd1306_init();
}

void run() {
    SSD1306.ssd1306_fillscreen(0);
    SSD1306.ssd1306_setpos(0, 1);
    SSD1306.ssd1306_string_font6x8("Hello world!");
}

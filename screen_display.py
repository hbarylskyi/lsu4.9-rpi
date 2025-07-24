import smbus2
import time

def display_on_screen(afr, temperature):
    """
    Displays the AFR and temperature on an I2C screen.

    :param afr: Air-Fuel Ratio to display.
    :param temperature: Temperature to display.
    """
    bus = smbus2.SMBus(1)  # Use I2C bus 1
    address = 0x3C  # I2C address of the screen

    # Example of sending data to the screen
    try:
        bus.write_byte_data(address, 0x00, 0x01)  # Clear display command
        time.sleep(0.1)
        message = f"AFR: {afr} Temp: {temperature}"
        for char in message:
            bus.write_byte_data(address, 0x40, ord(char))
            time.sleep(0.05)
    finally:
        bus.close()

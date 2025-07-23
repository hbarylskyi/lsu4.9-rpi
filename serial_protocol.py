import serial

def read_sensor_data(port='/dev/ttyS0', baudrate=115200):
    """
    Reads sensor data from a serial port.

    :param port: The serial port to read from.
    :param baudrate: The baud rate for the serial communication.
    :return: A tuple containing AFR and temperature.
    """
    ser = serial.Serial(port, baudrate, timeout=1)
    try:
        while True:
            if ser.in_waiting >= 8:
                data = ser.read(8)
                afr = data[0] * 0.1
                temperature = data[1]
                print(f"AFR: {afr}, Temperature: {temperature}")
    except KeyboardInterrupt:
        print("Stopping data read.")
    finally:
        ser.close()

if __name__ == "__main__":
    read_sensor_data()

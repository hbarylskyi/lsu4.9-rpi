import RPi.GPIO as GPIO
import socket

def read_sensor_data(gpio_pin=17):
    """
    Reads sensor data from a GPIO pin.

    :param gpio_pin: The GPIO pin number to read from.
    :return: A tuple containing AFR and temperature.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_pin, GPIO.IN)
    udp_ip = "192.168.1.5"
    udp_port = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    udp_ip = "192.168.1.5"
    udp_port = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        while True:
            # Simulate reading 8 bytes of data from GPIO
            data = [GPIO.input(gpio_pin) for _ in range(8)]
            afr = data[0] * 0.1
            temperature = data[1]
            message = f"AFR: {afr}, Temperature: {temperature}"
            print(message)
            sock.sendto(message.encode(), (udp_ip, udp_port))
        while True:
            if ser.in_waiting >= 8:
                data = ser.read(8)
                afr = data[0] * 0.1
                temperature = data[1]
                message = f"AFR: {afr}, Temperature: {temperature}"
                print(message)
                sock.sendto(message.encode(), (udp_ip, udp_port))
    except KeyboardInterrupt:
        print("Stopping data read.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    read_sensor_data()

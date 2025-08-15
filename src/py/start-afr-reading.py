import serial as pyserial
from screen import display_on_screen
import time
import threading

def process_packet(packet):
    """
    Processes an 8-byte packet from the serial stream.
    Expected packet structure:
      packet[1] = AFR * 10
      packet[2] = temperature offset (Celsius) with +740 added
    """
    if len(packet) != 8:
        print("Invalid packet length:", len(packet))
        return

    b = list(packet)

    # Decode values
    afr = b[1] * 0.1
    temp_c = b[2] + 740

    # Format as strings (if needed for display)
    afr_str = f"{afr:.1f}"
    temp_str = f"{temp_c:.1f}"

    # Print to console
    print(f"AFR: {afr_str}, Temp: {temp_str}°C")

    # Update display
    threading.Thread(target=display_on_screen, args=(afr_str, temp_str)).start()

def read_sensor_data(serial_port='/dev/ttyAMA0', baudrate=115200):
    """
    Reads sensor data from a serial port.

    :param serial_port: The serial port to read from.
    :param baudrate: The baud rate for the serial communication.
    :return: A tuple containing AFR and temperature.
    """
    # udp_ip = "192.168.1.5"
    # udp_port = 5005
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    ser = pyserial.Serial(serial_port, baudrate, 
                          #bytesize=pyserial.EIGHTBITS,
                          #parity=pyserial.PARITY_NONE,
                          #stopbits=pyserial.STOPBITS_ONE,
                          timeout=0)

    try:
        message = f"hi. will read data from {serial_port} at {baudrate} baud."
        print(message)
        
        display_on_screen(999, 999)

        buffer = bytearray()

        while True:
            waiting = ser.in_waiting
            
            if waiting == 0:
                time.sleep(0.001)
                continue

            print(f"[DEBUG] Bytes waiting in serial: {waiting}")
            print(f"[DEBUG] Buffer length before read: {len(buffer)}")

            data = ser.read(waiting)
            print(f"[DEBUG] Bytes read now: {len(data)}")

            buffer.extend(data)
            print(f"[DEBUG] Buffer length after read: {len(buffer)}")

            while len(buffer) >= 8:
                packet = buffer[:8]
                buffer = buffer[8:]
                print(f"[DEBUG] Processing packet, buffer length now: {len(buffer)}")
                process_packet(packet)
    except KeyboardInterrupt:
        print("Stopping data read.")
    finally:
        ser.close()

if __name__ == "__main__":
    read_sensor_data()

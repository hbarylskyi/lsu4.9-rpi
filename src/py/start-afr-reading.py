import serial
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

def open_serial(serial_port='/dev/ttyAMA0', baudrate=115200):
    while True:
        try:
            message = f"hi. will read data from {serial_port} at {baudrate} baud."
            print(message)
    
            ser = serial.Serial(serial_port, baudrate, timeout=0)
            ser.flushInput()  # clear any old bytes
            print(f"[INFO] Serial port {serial_port} opened.")
            return ser
        except serial.SerialException as e:
            print(f"[ERROR] Could not open serial port: {e}")
            time.sleep(2)  # retry every 2 seconds


def read_sensor_data():
    """
    Reads sensor data from a serial port.

    :param serial_port: The serial port to read from.
    :param baudrate: The baud rate for the serial communication.
    :return: A tuple containing AFR and temperature.
    """
    display_on_screen(999, 999)
    
    buffer = bytearray()
    ser = open_serial()

    while True:
        try:
            waiting = ser.in_waiting

            if waiting == 0:
                time.sleep(0.001)
                continue
            print(f"[DEBUG] Bytes waiting in serial: {waiting}")
            # Read whatever is in the serial buffer
            data = ser.read(waiting)
            buffer.extend(data)

            # Process complete packets
            while len(buffer) >= 8:
                packet = buffer[:8]
                buffer = buffer[8:]
                print(f"[DEBUG] Processing packet, buffer length now: {len(buffer)}")
                process_packet(packet)

        except serial.SerialException as e:
            print(f"[ERROR] Serial exception: {e}")
            try:
                ser.close()
            except:
                pass
            time.sleep(2)
            ser = open_serial()  # try to reopen automatically

        except KeyboardInterrupt:
            print("Stopping serial read.")
            try:
                ser.close()
            except:
                pass
            break

        # while True:
        #     waiting = ser.in_waiting
            
        #     if waiting == 0:
        #         time.sleep(0.001)
        #         continue

        #     # print(f"[DEBUG] Bytes waiting in serial: {waiting}")
        #     # print(f"[DEBUG] Buffer length before read: {len(buffer)}")

            
        #         # ser.flushInput()  # Clear input buffer before reading
        #     data = ser.read(waiting)
        #     # print(f"[DEBUG] Bytes read now: {len(data)}")

        #     buffer.extend(data)
        #     # print(f"[DEBUG] Buffer length after read: {len(buffer)}")

        #     while len(buffer) >= 8:
        #         packet = buffer[:8]
        #         buffer = buffer[8:]
        #         print(f"[DEBUG] Processing packet, buffer length now: {len(buffer)}")
        #         process_packet(packet)
    # except KeyboardInterrupt:
    #     print("Stopping data read.")
    # finally:
    #     ser.close()

if __name__ == "__main__":
    read_sensor_data()

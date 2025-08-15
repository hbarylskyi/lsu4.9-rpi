import serial as pyserial
from screen import display_on_screen
import time

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
    # display_on_screen(afr_str, temp_str)

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
            print(f"[DEBUG] Bytes waiting in serial: {waiting}")

            if waiting == 0:
                time.sleep(0.001)
                continue

            # Buffer length before reading
            print(f"[DEBUG] Buffer length before read: {len(buffer)}")

            # Read whatever is in the serial input buffer
            data = ser.read(waiting)
            print(f"[DEBUG] Bytes read now: {len(data)}")

            buffer.extend(data)
            print(f"[DEBUG] Buffer length after read: {len(buffer)}")

            # Process packets
            while len(buffer) >= 8:
                packet = buffer[:8]
                buffer = buffer[8:]
                print(f"[DEBUG] Processing packet, buffer length now: {len(buffer)}")
                process_packet(packet)

        # while True:
        #     if ser.in_waiting == 0:
        #         continue
        #     # Grab whatever is in the buffer right now
        #     data = ser.read(ser.in_waiting or 1)

        #     if data:
        #         print(f"in waiting: {ser.in_waiting}")
        #         print(len(buffer))
        #         print("buffer^^^ .. __")
        #         buffer.extend(data)

        #         # Process complete packets as they come
        #         while len(buffer) >= 8:
        #             packet = buffer[:8]
        #             buffer = buffer[8:]
            
        #             b = list(packet)
        #             afr = b[1] * 0.1
        #             temp_c = b[2] + 740
        #             print(f"AFR: {afr:.1f}, Temp: {temp_c}°C")

        #     time.sleep(0.005)
        
        '''
        while True:
            if ser.in_waiting >= 8:
                print(f"waiting {ser.in_waiting}")
                data = ser.read(8)
                print("read 8 bytes")
                # Convert bytes to integers
                b = list(data)

                # Check packet markers (optional validation)
                #if b[0] != 1 or b[3:] != [3, 4, 5, 6, 7]:
                #    print("Invalid packet:", b)
                #    continue
        
                afr = b[1] * 0.1
                temp_c = b[2] + 740  # final application temp
                
                afr_str = f"{afr:.1f}"
                temp_str = f"{temp_c:.1f}"
                # Print formatted values
                print(f"AFR: {afr:.1f}, Temp: {temp_c}°C")

                #data = ser.read(8)
                #afr = data[0] * 0.1
                #formatted_afr = f"{afr:.1f}"
                #temperature = data[1]

                #message = f"AFR: {formatted_afr}, Temperature: {temperature}"

                #display_on_screen(afr_str, temp_str)
    '''
    except KeyboardInterrupt:
        print("Stopping data read.")
    finally:
        ser.close()

if __name__ == "__main__":
    read_sensor_data()

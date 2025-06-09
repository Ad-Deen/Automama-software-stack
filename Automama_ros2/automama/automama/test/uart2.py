import serial
import time
import keyboard  # Requires sudo on Linux

# Open serial port
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
time.sleep(2)  # Wait for Arduino to reset

# Initial values
T = 0
S = 7
B = 7

try:
    while True:
        # Handle keypresses
        if keyboard.is_pressed('w'):
            T = min(255, T + 10)
            time.sleep(0.1)
        elif keyboard.is_pressed('s'):
            T = max(0, T - 10)
            time.sleep(0.1)
        elif keyboard.is_pressed('a'):
            S = max(0, S - 1)
            time.sleep(0.1)
        elif keyboard.is_pressed('d'):
            S = min(255, S + 1)
            time.sleep(0.1)
        elif keyboard.is_pressed('x'):
            B = min(255, B + 1)
            time.sleep(0.1)
        elif keyboard.is_pressed('c'):
            B = max(0, B - 1)
            time.sleep(0.1)
        elif keyboard.is_pressed('q'):
            print("Exiting...")
            break

        # Send 3-byte command
        msg = bytes([T, S, B])
        ser.write(msg)

        # Read response (3 bytes)
        if ser.in_waiting >= 3:
            response = ser.read(3)
            rx = list(response)
            
            print(f"Sent: [{T}, {S}, {B}] | Received: {rx}")

        time.sleep(0.05)  # 10 Hz

except KeyboardInterrupt:
    print("Interrupted")

finally:
    ser.close()
    print("Serial port closed")

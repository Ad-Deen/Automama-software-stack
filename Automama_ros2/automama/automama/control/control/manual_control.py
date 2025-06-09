#!/usr/bin/env python3

"""
ROS 2 Node: UART Keyboard Controller

This node sends 3-byte throttle, steering, and brake commands to an Arduino over serial
based on real-time keyboard inputs.

📦 Requirements:
- pyserial (`pip install pyserial`)
- pynput (`pip install pynput`)

🎮 Keyboard Controls:
  w → Increase throttle (+10)
  s → Decrease throttle (-10)
  a → Steer left (-1)
  d → Steer right (+1)
  x → Increase brake (+1)
  c → Decrease brake (-1)
  q → Quit the node

⚠️ Notes:
- Does NOT require root privileges on Linux.
- Set the correct serial port (`/dev/ttyUSB0`) if needed.
"""

import rclpy
from rclpy.node import Node
import serial
import time
from pynput import keyboard

class UARTKeyboardController(Node):
    def __init__(self):
        super().__init__('uart_keyboard_controller')

        # Serial port configuration
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
            time.sleep(2)  # Wait for Arduino to reset
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to open serial port: {e}")
            raise SystemExit

        # Initial T, S, B values
        self.T = 0  # Throttle
        self.S = 6  # Steering
        self.B = 7  # Brake

        self.running = True

        # Start keyboard listener
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

        # Start main timer loop at 20 Hz
        self.timer = self.create_timer(0.05, self.loop)

    def on_press(self, key):
        try:
            k = key.char.lower()
        except AttributeError:
            return  # Special keys like shift etc.

        if k == 'w':
            self.T = min(150, self.T + 1)
        elif k == 's':
            self.T = max(0, self.T - 10)
        elif k == 'a':
            self.S = max(0, self.S - 1)
        elif k == 'd':
            self.S = min(12, self.S + 1)
        elif k == 'x':
            self.B = min(17, self.B + 1)
        elif k == 'c':
            self.B = max(7, self.B - 1)
        elif k == 'q':
            self.get_logger().info("Quit key pressed, shutting down...")
            self.running = False
            rclpy.shutdown()

    def loop(self):
        if not self.running:
            return

        try:
            # Clamp values to valid ranges
            # self.T = max(80, min(150, self.T))  # Clamp T to [80, 150]
            # self.S = max(0, min(14, self.S))    # Clamp S to [0, 14]
            # self.B = max(7, min(18, self.B))    # Clamp B to [7, 18]

            # Send command
            msg = bytes([self.T, self.S, self.B])
            self.ser.write(msg)

            # Read 3-byte feedback
            if self.ser.in_waiting >= 3:
                response = self.ser.read(3)
                rx = list(response)
                self.get_logger().info(f"Sent: [{self.T}, {self.S}, {self.B}] | Received: {rx}")

        except Exception as e:
            self.get_logger().error(f"Error: {e}")
            rclpy.shutdown()

    def destroy_node(self):
        self.listener.stop()
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()
            self.get_logger().info("Serial port closed")
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = UARTKeyboardController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Interrupted by user")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

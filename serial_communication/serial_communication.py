import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 1.0)
time.sleep(3)
ser.reset_input_buffer()
print("serial OK")

try:
    while True:
        time.sleep(1)
        print("send msg to arduino")
        ser.write("Hello from raspberrypi\n".encode('utf-8'))

except KeyboardInterrupt:
    print("closed serial communication")
    ser.close()
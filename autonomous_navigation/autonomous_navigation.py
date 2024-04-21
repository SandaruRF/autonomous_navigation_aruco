import numpy as np
import serial
import time
import cv2
from picamera2 import Picamera2

ser = serial.Serial('/dev/ttyACM0', 115200, timeout = 1.0)
time.sleep(3)
ser.reset_input_buffer()
print("serial OK")

FPS = 0
START_TIME = time.time()

ARUCO_DICT = {
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000
}

directions = {
    1: "East",
    2: "South-East",
    3: "South",
    4: "South-West",
    5: "West",
    6: "North-West",
    7: "North",
    8: "North-East",
    0: "STOP"
}
default_value = "Unknown" #incase detect any other markerID

def aruco_display(corners, ids, rejected, image):
    if len(corners) > 0:
        ids = ids.flatten()
        for (markerCorner, markerID) in zip(corners, ids):
            corners = markerCorner.reshape((4,2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            cv2.line(image, topLeft, topRight, (0,255,0), 2)
            cv2.line(image, topRight, bottomRight, (0,255,0), 2)
            cv2.line(image, bottomRight, bottomLeft, (0,255,0), 2)
            cv2.line(image, bottomLeft, topLeft, (0,255,0), 2)

            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(image, (cX, cY), 4, (0,0,255), -1)
            
            
            direction = directions.get(markerID, default_value)
            cv2.putText(image, str(markerID)+": ", (topLeft[0], topLeft[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)
            cv2.putText(image, direction, (topLeft[0] + 20, topLeft[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)
            #print("[Inference] ArUco marker ID: {}".format(markerID))
            
            time.sleep(0.01)
            msg = direction+"\n"
            print(msg);
            ser.write(msg.encode('utf-8')) #send detected direction to arduino
            global camera_active
            if camera_active and direction != "Unknown":
                camera_active = False
                print("Camera deactivated")
                picam2.stop()
                picam2.close()
                cv2.destroyAllWindows()
                print("hey")

    return image

aruco_type = "DICT_4X4_1000"

arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[aruco_type])

arucoParams = cv2.aruco.DetectorParameters_create()

camera_active = False

while True:
    if ser.in_waiting > 0:
        message = ser.readline().decode('utf-8').rstrip()
        print(message)
        if message == "Start":
            if not camera_active:
                camera_active = True
                print("Camera activated")
                picam2 = Picamera2()
                picam2.preview_configuration.main.size = (640, 480)
                picam2.preview_configuration.main.format = "RGB888"
                picam2.preview_configuration.align()
                picam2.configure("preview")
                picam2.start()
#         elif message == "Stop":
#             if camera_active:
#                 camera_active = False
#                 print("Camera deactivated")
#                 picam2.stop()
#                 picam2.close()
#                 cv2.destroyAllWindows()
                
    if camera_active:
        image = picam2.capture_array()
        image = cv2.flip(image, -1)

        h, w, _ = image.shape

        width = 320
        height = int(width*(h/w))
        image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)

        corners, ids, rejected = cv2.aruco.detectMarkers(image, arucoDict, parameters = arucoParams)

        detected_markers = aruco_display(corners, ids, rejected, image)
        
        

        fps_text = 'FPS = {:.1f}'.format(FPS)
        cv2.putText(image, fps_text, (24, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0,255,0), 1, cv2.LINE_AA)
        FPS = 0.9*FPS + 0.1*(1 / (time.time() - START_TIME))
        START_TIME = time.time()
        
        cv2.imshow("Image", detected_markers)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

print("serial communication closed")
ser.close()
cv2.destroyAllWindows()


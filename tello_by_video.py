import module.tello_module as tello
import module.tello_module_binary as tello_b
from concurrent.futures import ThreadPoolExecutor as TPE
from getch import getch
import time
import math
import numpy as np
import cv2

video = None
udp_msg = tello.udp(('192.168.10.1', 8889))
binary_cmd = tello_b.tello_binary()
flag = True
executor = TPE(max_workers=3)

def input_key():
    input_ = getch()
    try:
        input_ = input_.decode('UTF-8')
    except:
        pass
    return input_

def stream():
    while True:
        if not flag:
            break
        cv2.waitKey(1)
        frame = video.display()
        cv2.imshow('Tello Streaming', frame)
    cv2.destroyAllWindows()

def drone(code):
    udp_msg.send(code)

def background():
    while flag:
        udp_msg.send(binary_cmd.main())
        time.sleep(0.1)
def hover():
    while flag:
        udp_msg.send('command')
        time.sleep(10)

yaw, thr, pitch, roll = IMU = (0, 0, 0, 0)

def main():
    executor.submit(hover)
    executor.submit(background)
    drone('streamon')
    global video
    video = tello.video(('192.168.10.1', 11111), (864, 576), 15)
    executor.submit(stream)
    while True:
        c = input_key()
        if c == 'e':
            break
        elif c == '0':
            binary_cmd.setIMU((0, 0, 0, 0))
        elif c == 'j':
            binary_cmd.setIMU((0, 0, 0, 0))
            drone(binary_cmd.takeoff)    
        elif c == 'k':
            binary_cmd.setIMU((0, 0, 0, 0))
            drone(binary_cmd.land)
            
        elif c == 'w':
            binary_cmd.setIMU((0, 0, 500, 0))
        elif c == 'x':
            binary_cmd.setIMU((0, 0, -500, 0))
        elif c == 'a':
            binary_cmd.setIMU((0, 0, 0, -500))
        elif c == 'd':
            binary_cmd.setIMU((0, 0, 0, 500))
        elif c == 'n':
            binary_cmd.setIMU((0, 500, 0, 0))
        elif c == 'm':
            binary_cmd.setIMU((0, -500, 0, 0))
        elif c == 's':
            binary_cmd.setIMU((500, 0, 0, 0))

        elif c == 'p':
            for i in range(10):
                for n in range(9):
                    yaw = 0
                    thr = round(500*math.sin(math.radians(45*n)))
                    pitch = 0
                    roll = round(500*math.cos(math.radians(45*n)))
                    binary_cmd.setIMU((yaw, thr, pitch, roll))
                    time.sleep(0.5)
            binary_cmd.setIMU((0, 0, 0, 0))
        else:
            pass
    print('')
    global flag
    flag = False
    drone('streamoff')
    drone(binary_cmd.land)

if __name__ == "__main__":
    main()
    executor.shutdown()

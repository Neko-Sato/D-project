#The name of this module is "tello_module"
#Please use the next code for import
#"import tello_module as tello"
import socket
import time
import cv2
import numpy as np
from datetime import datetime

class udp:
    def __init__(self, address):
        self.ip, self.port = address
        self.address = ('', self.port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.address)
        self.sock.settimeout(1.0)
        self.data = b''
    def recv(self):
            try:
                data, server = self.sock.recvfrom(5000)
            except socket.timeout:
                data = b'' 
            self.data = data
    def send(self, msg):
        if not type(msg) == bytes:
            msg = msg.encode('utf-8')
        self.sock.sendto(msg, (self.ip, self.port))

class video:
    def __init__(self, address, resolution, fps):
        self.flag = True
        self.ip, self.port = address
        self.addr = 'udp://' + self.ip + ':' + str(self.port)
        self.width, self.height = resolution
        self.fps = fps
        self.frame = np.zeros((self.height, self.width, 3), np.uint8)
        self.cap = cv2.VideoCapture(self.addr)
        #ret = self.cap.set(3, self.width)
        #ret = self.cap.set(4, self.height)
        ret = self.cap.set(5, self.fps)
    def display(self):
        try:
            ret, image = self.cap.read()
            if ret == True:
                self.frame = cv2.resize(image, (self.width, self.height))
        except:
            pass
        return self.frame
    def save(self):
        fourcc = cv2.VideoWriter_fourcc(*'XIVE')
        self.out_tuple = ('video/output_' + str(datetime.now().strftime("%Y.%m.%d.%H.%M.%S")) + '.mp4', fourcc, self.fps, (self.width, self.height+50))     
    def end(self):
        self.flag = False
        self.cap.release()

if __name__ == "__main__":
    pass

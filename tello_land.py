import module.tello_module as tello
import time

flag = True
udp_msg = tello.udp(('192.168.10.1', 8889))

def main():
    udp_msg.send('land')

if __name__ == "__main__":
    main()

import module.tello_module as tello
import module.tello_module_control as tello_c
import module.tello_module_GPI as tello_g
from concurrent.futures import ThreadPoolExecutor as TPE
from concurrent.futures import ThreadPoolExecutor as PPE
import numpy as np
import copy
import cv2
import time

udp_msg = tello.udp(('192.168.10.1', 8889))
udp_state = tello.udp(('', 8890))
video = None
twin = tello_g.window()
flag = True
to_code = tello_c.cmd.p_1
send_msg = ''
executor = TPE(max_workers=3)
executor_ = PPE(max_workers=1)

def drone(code):
    global send_msg
    send_msg = code
    twin.send.set(code)
    udp_msg.send(code)
    time.sleep(1)
    send_msg = ''
    twin.send.set('')

def stream():
    video.save()
    output = cv2.VideoWriter(*video.out_tuple)
    white = np.full((50, video.width, 3), 255, np.uint8)
    font = cv2.FONT_HERSHEY_DUPLEX
    #count = 0
    #c_max = 8
    while True:
        if not video.flag == True:
            break
        cv2.waitKey(1)
        frame = video.display()
        
        #if count%c_max == 0:
        #    pass

        frame_msg = copy.deepcopy(white)
        txt = udp_msg.data.decode('utf-8')
        cv2.putText(frame_msg, '[send] ' + send_msg, (10, 15), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame_msg, '[recv] ' + txt, (10, 40), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        frame = cv2.vconcat([frame, frame_msg])
        
        output.write(frame) #save
        cv2.imshow('Tello Streaming', frame) #display
        
        #if count == c_max:
        #    count = 1
        #count = count + 1
    output.release()
    cv2.destroyAllWindows()

def display_data():
    while True:
        if not flag:
            break
        udp_msg.recv()
        udp_state.recv()
        if not udp_msg.data == b'':
            twin.recv.set(udp_msg.data.decode('utf-8').rstrip())
        else:
            twin.recv.set('')
        if not udp_state.data == b'':
            state = udp_state.data.rstrip().decode('utf-8')
            state_bat = state[state.find('bat')+4:state.find('baro')-1]
            twin.root.title('Tello Control - battery : ' + state_bat + '%')
        else:
            twin.root.title('Tello Control')
            
def main():
    executor.submit(twin.main)
    time.sleep(0.1)
    twin.EditBox.configure(state='readonly')
    twin.Button.configure(state='disabled')
    executor.submit(display_data)
    twin.noticet.set('wait...')
    drone('command')
    drone('streamon')
    global video
    video = tello.video(('192.168.10.1', 11111), (864, 576), 15)
    executor_.submit(stream)
    c = ''
    while True:
        twin.EditBox.configure(state='normal')
        twin.Button.configure(state='normal')
        twin.noticet.set('Please enter the command (Input e to end)')
        while twin.msg == '':
            pass
        twin.EditBox.configure(state='readonly')
        twin.Button.configure(state='disabled')
        twin.noticet.set('wait...')
        c = twin.msg
        twin.msg = ''
        if c == 'e' :
            break
        if c == 'streamon' or c == 'streamoff':
            twin.noticet.set('...NO!')
            time.sleep(0.5)
            continue
        if c == 't': #using txet-file
            try:
                twin.noticet.set('...Enter file name')
                twin.EditBox.configure(state='normal')
                twin.Button.configure(state='normal')
                while twin.msg == '':
                   pass
                twin.EditBox.configure(state='readonly')
                twin.Button.configure(state='disabled')
                f = open('text/' + twin.msg + '.txt')
                twin.noticet.set('wait...')
                twin.msg = ''
                line = f.readline()
                twin.EditBox.configure(state='normal')
                twin.Button.configure(state='normal')
                while line:
                    text_cmd = line.rstrip()
                    if twin.msg == 'c':
                        twin.EditBox.configure(state='readonly')
                        twin.Button.configure(state='disabled')
                        twin.msg = ''
                        break
                    if not text_cmd.find('sleeping'):
                        twin.noticet.set('sleeping ' + text_cmd[9:len(text_cmd)] + 's')
                        time.sleep(float(text_cmd[9:len(text_cmd)]))
                        twin.noticet.set('wait...')
                        line = f.readline()
                        continue
                    elif not text_cmd[0:1].find('#'):
                        line = f.readline()
                        continue
                    drone(text_cmd)
                    line = f.readline()
                f.close
            except:
                twin.noticet.set('Not Find')
                twin.msg = ''
                time.sleep(0.5)
            continue
        c = to_code(c)
        drone(c)
    global flag
    flag = False
    video.end()
    drone('streamoff')
    drone('land')
    twin.end()

if __name__ == "__main__":
    main()
    executor.shutdown()

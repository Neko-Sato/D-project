import module.tello_module as tello
import module.tello_module_control as tello_c
import module.tello_module_GPI as tello_g
from concurrent.futures import ThreadPoolExecutor as TPE
import numpy as np
import time
from datetime import datetime

udp_msg = tello.udp(('192.168.10.1', 8889))
udp_state = tello.udp(('', 8890))
twin = tello_g.window()
flag = True
to_code = tello_c.cmd.p_1
executor = TPE(max_workers=2)

def drone(code):
    twin.send.set(code)
    udp_msg.send(code)
    time.sleep(1)
    twin.send.set('')

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
            print(udp_state.data)
        if not udp_state.data == b'':
            state = udp_state.data.decode('utf-8').rstrip()
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
                time.sleep(1)
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
    drone('streamoff')
    drone('land')
    twin.end()
    
if __name__ == "__main__":
    main()
    executor.shutdown()

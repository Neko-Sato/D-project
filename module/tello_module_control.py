#The name of this module is "tello_module_control"
#Please use the next code for import
#"import tello_module_control as tello_c"

class cmd:
    def p_1(c):
        a = c
        if c[1:2] == ' ':
            if c[2:3] == '-':
                l = 3
            else:
                l = 2
            if c[l:len(c)].isdecimal():
                if not c[0:1].find('n'):
                    a = 'up ' + c[2:len(c)]
                elif not c[0:1].find('m'):
                    a = 'down ' + c[2:len(c)]
                elif not c[0:1].find('w'):
                    a = 'forward ' + c[2:len(c)]
                elif not c[0:1].find('x'):
                    a = 'back ' + c[2:len(c)]
                elif not c[0:1].find('a'):
                    a = 'left ' + c[2:len(c)]
                elif not c[0:1].find('d'):
                    a = 'right ' + c[2:len(c)]
                elif not c[0:1].find('s'):
                    a = 'cw ' + c[2:len(c)]
            elif c[2:len(c)].isalpha():
                if len(c[2:len(c)]) == 1:
                    if not c[0:1].find('f'):
                        f = ''
                        if c[2:len(c)] == 'w':
                            f = 'f'
                        elif c[2:len(c)] == 'x':
                            f = 'b'
                        elif c[2:len(c)] == 'a':
                            f = 'l'
                        elif c[2:len(c)] == 'd':
                            f = 'r'
                        a = 'flip ' + f
        elif c == 'j' :
            a = 'takeoff'
        elif c == 'k' :
            a = 'land'
        elif c == 'b' :
            a = 'battery?'
        return a

if __name__ == "__main__":
    pass

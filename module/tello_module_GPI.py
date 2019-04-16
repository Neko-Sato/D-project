#The name of this module is "tello_module_GPI"
#Please use the next code for import
#"import tello_module_GPI as tello_g"

import tkinter as tk
import time

class window:
    def main(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", (lambda: 'pass'))
        self.root.resizable(0,0)

        self.msg = ''
        
        self.noticet = tk.StringVar()
        self.noticet.set('')
        self.send = tk.StringVar()
        self.send.set('')
        self.recv = tk.StringVar()
        
        self.root.title('Tello Control')
        self.root.geometry("400x150")
        self.object()
        self.root.mainloop()

    def object(self):
        self.notice_title = tk.Label(text='[notice]', width=5)
        self.notice_title.grid(padx=2, ipadx=7, pady=5, sticky=tk.W, row=1, column=1)

        self.notice_label = tk.Label(textvariable=self.noticet, width=45, bg='white', relief='ridge')
        self.notice_label.grid(padx=2, pady=5, sticky=tk.W, row=1, column=2, columnspan=2)


        self.send_title = tk.Label(text='[send]', width=5)
        self.send_title.grid(padx=2, ipadx=7, pady=5, sticky=tk.W, row=2, column=1)

        self.send_label = tk.Label(textvariable=self.send, width=45, bg='white', relief='ridge')
        self.send_label.grid(padx=2, pady=5, sticky=tk.W, row=2, column=2, columnspan=2)


        self.recv_title = tk.Label(text='[recv]', width=5)
        self.recv_title.grid(padx=2, ipadx=7, pady=5, sticky=tk.W, row=3, column=1)

        self.recv_label = tk.Label(textvariable=self.recv, width=45, bg='white', relief='ridge')
        self.recv_label.grid(padx=2, pady=5, sticky=tk.W, row=3, column=2, columnspan=2)


        self.EditBox = tk.Entry(width=55)
        self.EditBox.insert(tk.END,"")
        self.EditBox.bind('<Return>', self.DeleteEntryValue) 
        self.EditBox.grid(padx=5, pady=5, sticky=tk.W, row=4, column=1, columnspan=2)
        
        self.Button = tk.Button(text='Send', width=5)
        self.Button.bind("<Button-1>", self.DeleteEntryValue)
        self.Button.grid(padx=5, pady=5, sticky=tk.W, row=4, column=3)

    def DeleteEntryValue(self, event):
        self.msg = self.EditBox.get()
        self.EditBox.delete(0, tk.END)

    def end(self):
        self.noticet.set('')
        self.send.set('')
        self.recv.set('')
        self.EditBox.delete(0, tk.END)
        
        self.noticet.set('See You Good Bye...')
        time.sleep(0.3)
        self.send.set('...')
        time.sleep(0.3)
        self.recv.set('Exit...')
        time.sleep(0.3)
        self.root.quit()

if __name__ == "__main__":
    pass


import Tkinter as tk


from chating.frame_chat_window import MqttChatingFrame


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, 
                          master)
        self.pack(expand=True, anchor=tk.CENTER, fill=tk.BOTH)  
        self.frame_chat_window = MqttChatingFrame(master=self)
        self._pack_main(self.frame_chat_window)
        
    def _pack_main(self, frame):
        frame.pack(expand=True, anchor=tk.CENTER, fill=tk.BOTH)
    
def start(): 
    main_window = Application()
    win_top = main_window.master
    win_top.title('MQTT Station')
    win_top.minsize(600, 400)
    win_top.update()

    current_window_width = win_top.winfo_width()
    current_window_height = win_top.winfo_height()    
    screen_width, screen_height = win_top.maxsize()
    temp = '%dx%d+%d+%d' % (current_window_width, current_window_height, 
                            (screen_width - current_window_width) / 2,
                            (screen_height - current_window_height) / 2)     
    win_top.geometry(temp)

    main_window.mainloop()
    
if __name__ == '__main__':
    start()
# -*- coding:utf-8 -*-
'''
Created on 2016/3/3

@author: xinfeng.yang
'''
import os 
import urlparse
import mosquitto
import chating
import threading
import ttk
import Tkinter as tk


__version__ = "1.0.0"
__author__ = "xinfeng.yang"
__all__ = ["MqttChatingFrame"]

class MqttChatingFrame(tk.Frame):
    def __init__(self, master=None, logout=None):
        tk.Frame.__init__(self, master)        
        self._logout_fun = logout 
        self.__creat_text()
        self.__creat_button()
        self.__config_layout()

    def __creat_text(self): 
        self._receive_message = tk.Text(self, height=20)
        self._receive_message.grid(row=0, pady=5, sticky=tk.NSEW)
        self._send_message = tk.Text(self, height=12)
        self._send_message.grid(row=2, pady=5, sticky=tk.NSEW)
        self._send_message.bind('<Key-Return>', self.__send_message)
        
    def __creat_button(self):
        ttk.Button(self, text='History Record').grid(row=1, padx=8, sticky=tk.E)
        ttk.Button(self, text='Send').grid(row=3, padx=8, sticky=tk.E)
        
    def __config_layout(self):
        self.rowconfigure(0, weight=1) 
        self.columnconfigure(0, weight=1) 
        
    def __send_message(self, event):
        _context = self._send_message.get(0.0, tk.END)
        threading.Thread(target=mqtt(_context)).start() 
            
        self._receive_message.insert(tk.END, _context)
        self._send_message.delete(0.0, tk.END)

        
def mqtt(message):
    def on_connect(mosq, obj, rc):
        print("rc: " + str(rc))
     
    def on_message(mosq, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
     
    def on_publish(mosq, obj, mid):
        print("mid: " + str(mid))
     
    def on_subscribe(mosq, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))
     
    def on_log(mosq, obj, level, string):
        print(string)
 
    mqttc = mosquitto.Mosquitto()
    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
     
    # Uncomment to enable debug messages
    #mqttc.on_log = on_log
     
    # Parse CLOUDMQTT_URL (or fallback to localhost)
    url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://hngfyccr:0_TmNrRbNplw@m10.cloudmqtt.com:18717')
    url = urlparse.urlparse(url_str)
     
    # Connect
    mqttc.username_pw_set(url.username, url.password)
    mqttc.connect(url.hostname, url.port)
     
    # Start subscribe, with QoS level 0
    mqttc.subscribe("hello/world", 0)
     
    # Publish a message
    mqttc.publish("hello/world", "{0}:{1}".format(chating.USER, message))
     
    # Continue the network loop, exit when an error occurs
    rc = 0
    while rc == 0:
        rc = mqttc.loop()
    print("rc: " + str(rc))
        
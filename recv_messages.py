# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 04:51:31 2019

@author: Xkalaber
"""

import threading
import os, sys

class RecvMessages(threading.Thread):
    def __init__(self,client_socket):
        threading.Thread.__init__(self)
        self.client_socket=client_socket
    def run(self):
        while True:
            try:
                msg=self.client_socket.recv(1500)
            except:
                sys.exit()
            if len(msg):
                print(msg.decode(),end='')
            else:
                print('[other side closed socket, shutting down]')
                self.client_socket.close()
                os._exit(0)
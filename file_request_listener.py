# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 04:55:00 2019

@author: Xkalaber
"""

import threading

import os

class FileRequestListener(threading.Thread):
    def __init__(self,serversocket):
        threading.Thread.__init__(self)
        self.serversocket=serversocket
    def run(self):
        while True:
            try:
                sock,addr=self.serversocket.accept()
                filename=sock.recv(1500).decode()
                print('received request for file: ' +filename)
                file_stat=os.stat(filename)
                if file_stat.st_size:
                    file=open(filename,'rb')
                    while True:
                        file_bytes=file.read(1024)
                        if file_bytes:
                            sock.send(file_bytes)
                        else:
                            break
                    file.close()
                else:
                    pass
                sock.close()
            except OSError:
                pass
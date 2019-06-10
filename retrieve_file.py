# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 04:35:25 2019

@author: Xkalaber
"""

import threading
import os,sys,socket

class RetrieveFile(threading.Thread):
    def __init__(self,hostname,port,filename):
        threading.Thread.__init__(self)
        self.hostname=hostname
        self.port=port
        self.filename=filename
    def run(self):
        sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.hostname:
            print('connecting to other side; hostname: '+self.hostname)
            sock.connect((self.hostname,int(self.port)))
        else:
            print('connecting to other side; hostname: localhost')
            sock.connect(('localhost',int(self.port)))
        try:
            sock.send(self.filename.encode())
        except:
            sys.exit()
        file=open(self.filename,'wb')
        while True:
            try:
                file_bytes=sock.recv(1500)
            except:
                break
            if len(file_bytes):
                file.write(file_bytes)
            else:
                sock.close()
                break
        file.close()
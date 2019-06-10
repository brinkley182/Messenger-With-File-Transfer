# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 04:01:43 2019

@author: Xkalaber
"""


def connectToServer(port,server):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    if server:
        sock.connect((server,int(port)))
    else:
        sock.connect(('localhost',int(port)))
    return sock
def createServerSocket(port):
    serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    serversocket.bind(('',int(port)))
    serversocket.listen(5)
    return serversocket
def displayMenu():
    print("Enter an option ('m', 'f', 'x'):\n (M)essage (send)\n (F)ile (request) \n e(X)it")
def getConnectPort(sock):
    global conect_port
    msg_bytes=sock.recv(1500)
    if len(msg_bytes):
        connect_port=msg_bytes.decode()
    else:
        sock.close()
        return None
    return 1
def getOption():
    response=sys.stdin.readline()
    if not response:
        return None
    return response[0]
def requestFile(hostname,port):
    print('Which file do you want? ')
    filename=sys.stdin.readline().rstrip()
    if not filename:
        return None
    RetrieveFile(hostname,port,filename).start()
    return 1
def sendMessage(sock):
    print('Enter your message: ')
    msg= sys.stdin.readline()
    if not msg:
        return None
    try:
        sock.send(msg.encode())
    except:
        return None
    return 1
def sendListeningPort(sock):
    global listen_port
    try:
        sock.send(listen_port.encode())
    except:
        return None
    return 1
def usage(script_name):
    print('Usage: py' + script_name +'-l <listening port number> [-s] [<server address>] [-p] [<server port>]')
if __name__=="__main__":
    import sys, os
    import socket
    argc=len(sys.argv)
    if argc<3 or argc>7:
        usage(sys.argv[0])
        print('args')
        sys.exit()
    import getopt
    optlist, non_option_args=getopt.getopt(sys.argv[1:],'l:s:p:')
    act_as_server=False
    listen_port=None
    connect_server=None
    connect_port=None
    for opt, arg in optlist:
        if opt=='-l':
            listen_port=arg
        if opt=='-s':
            connect_server=arg
        if opt=='-p':
            connect_port=arg
    if not listen_port:
        usage(sys.argv[0])
        sys.exit()
    serversocket=createServerSocket(listen_port)
    if not connect_port:
        act_as_server=True
    if act_as_server:
        sock, addr=serversocket.accept()
        connect_server=addr[0]
        if not getConnectPort(sock):
            serversocket.close()
            sys.exit()
    else:
        sock=connectToServer(connect_port,connect_server)
        if not sendListeningPort(sock):
            serversocket.close()
            sys.exit()
    from recv_messages import RecvMessages
    RecvMessages(sock).start()
    from file_request_listener import FileRequestListener
    FileRequestListener(serversocket).start()
    from retrieve_file import RetrieveFile
    while True:
        displayMenu()
        option=getOption()
        if not option:
            break
        if option=='m':
            if not sendMessage(sock):
                break
        elif option=='f':
            if not requestFile(connect_server, connect_port):
                break
        elif option =='x':
            break
        else:
            print('Invalid option')
    try:
        sock.shutdown(socket.SHUT_WR)
        sock.close()
        serversocket.close()
        os._exit(0)
    except:
        pass
            
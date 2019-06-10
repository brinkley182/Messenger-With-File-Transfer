import sys
import socket
import threading
import os
import struct

#Sending thread

class Sen(threading.Thread):
    def __init__(self, soc):
        threading.Thread.__init__(self)
        self.soc=soc
    def run(self):
		#infinite loop handling sending threads
        while True:	
            print("Enter an option ('m', 'f', 'x'):\n (M)essage (send)\n (F)ile (request) \n e(X)it")
            option=input()
            if(option=='m'):
                print("Enter your message")
			#takes in message catches at end of file
                try:		
                    message = input()
        					#sends to either server or client
                    self.soc.sendall(message.encode())
                except EOFError:
                    os._exit(0)
            elif(option=='f'):
                self.soc.sendall('f'.encode())
                print("Enter your filename")
                filename=input()
                self.soc.sendall(filename.encode())
                if(".txt" in filename):
                    file_size=self.soc.recv(1).decode()
                    if message == '0':
                        print("file does not exist or is empty")
                    else:
                        requestFileBin(self.soc,filename)
                else:
                    file_size=self.soc.recv(4)
                    if file_size:
                        size=struct.unpack('!L', file_size[:4])[0]
                        if size:
                            requestFileBin(self.soc,filename)
                        else:
                            print("file does not exist or is empty")
                    else:
                        print("file does not exist or is empty")
            elif(option=='x'):
                self.soc.close()
                os._exit(0)
            else:
                print('Invalid option try again')
def requestFileBin(sock, filename):
    file=open(filename,'wb')
    while True:
        file_bytes=sock.recv(1024)
        if file_bytes:
            print(file_bytes)
            file.write(file_bytes)
        else:
            break
    file.close()
def sendFileBin(sock, filename):
	try:
		file_stat= os.stat( filename )
		file_exists= True
	except FileNotFoundError:
		file_exists= False
	if (not file_exists) or (file_stat.st_size == 0):
		sock.send( '0'.encode() )
		sys.exit()
	sock.send( '1'.encode() )
	# open the file
	file= open( filename )
	# read the file and transmit its contents
	for line in file:
		sock.send( line.encode() )
		
				
				
#Receiving thread
class Rec(threading.Thread):
	#initializes self
    def __init__(self,soc):
        threading.Thread.__init__(self)
        self.soc=soc
	#starts thread	
    def run(self):
		#infinite loop handling receiving messages
        while True:
            option=self.soc.recv(1).decode()
            if option == 'm':
                data = self.soc.recv(1024).decode()  # receive response
    			#prints data
                print(str(data))
            elif option == 'f':
                filename=self.soc.recv(1024).decode()
                print(filename)
                sendFileBin(self.soc,filename)
            elif option =='x':
                print('Client has disconnected')
                self.soc.close()
	#def sendFile(sock,file_size,file)
#launches server and creates server threads
def server_program(port, host):
    #instantiates socket stream needed for the pipes
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((host, port))  # bind host address and port together
    # configure how many client the server can listen simultaneously
	server_socket.listen(5)
	while True:
		conn, address = server_socket.accept()  # accept new connection
        #creates a server receive thread and starts it
		serv_rec= Rec( conn)
		serv_rec.start()
		#creates a server thread that sends to client
		serv_send= Sen( conn)
		serv_send.start()
		#end of thread, server constantly receiving only worried about ending send to open space
		sys.exit()
	conn.close()  # close the connection
#creates client threads and connects to server host
def client_program(port, host):
	conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
	conn.connect((host, port))  # connect to the server
	#clientConn= socket.socket(socket.AF_INET, socket.SOCK_STREAM)


	#infinite loop creating threads
	while True:
		#sends from client
		cli_send= Sen( conn)
		cli_send.start()
		#receives from server
		cli_rec= Rec( conn)
		cli_rec.start()
		#Only worried about ending receiving since clients are typically sending
		sys.exit()
	conn.close()  # close the connection



#main function handles command line
if __name__ == '__main__':
	#takes in command line arguments	
	args = sys.argv
	#initializing booleans and gets host
	server=False
	client=False
	hostAddress= socket.gethostname()
	#print("Arguments: "+args[0]+" "+args[1]+" "+args[2])
	#Checks for number of arguments
	if(len(args)==3):
		print(args)
		#checks if server
		if(args[1]=="-l"):
			#sets port and tells if server catches invalid inputs			
			try:
				serverPort = int(args[2])
				server=True
			except ValueError:
				print("Port Number Should contain only numbers")
		#host address never given only if not server then is client
		else:
			#sets port and checks if input is valid
			try:
				portAddress = int(args[1])
			except ValueError:
				print("Port Number Should contain only numbers")
			#sees if host address exists and sets client to true catching invalid inputs
			try:
				hostAddress= args[2]
				client=True
			except socket.error:
				print("Server address is invalid.")
	#else if the length of command line is only 2 can only be client
	elif(len(args)==5):
		#tells if client sets port and checks if input is valid
		try:
			clientPort=int(args[2])
			serverPort= int(args[4])
			client = True
		except ValueError:
			print("Port Number should contain only numbers") 
	#else command line values were invalid
	else:
		print(len(args))
		print("\ninvalid number of arguments")  
 	#starts server
	if (server==True):
		server_program(serverPort, hostAddress)
	#starts client
	elif (client==True):
		client_program(serverPort, hostAddress)

from ctypes.wintypes import SIZE
from email import message
import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)      # For UDP
udp_host = socket.gethostname()		        # Host IP
udp_port = 12345			                # specified port to connect
SIZE = 4096
sock.bind((udp_host,udp_port))
message = ''
while True:
	print ("Waiting for client...")
	data = sock.recvfrom(SIZE)    
	message = data[0].decode("utf-8")
	if(message=='FILESENDING'):
		file_name = sock.recvfrom(SIZE)
		file_name  = file_name[0].decode("utf-8")
		file = open(("received_folder/"+file_name),"wb")
		data = sock.recvfrom(SIZE)
		file.write(data[0])
		while(len(data[0])>=SIZE):
			data = sock.recvfrom(SIZE)
			file.write(data[0])
		file.close()
		print("FILE Transferred Completed")

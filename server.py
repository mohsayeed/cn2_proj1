import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)      # For UDP
udp_host = socket.gethostname()		        # Host IP
udp_port = 12345			                # specified port to connect
sock.bind((udp_host,udp_port))
while True:
	print ("Waiting for client...")
	data = sock.recvfrom(1024)    
	print ("Received Messages:",data[0].decode("utf-8"))

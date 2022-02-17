import socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udp_host = socket.gethostname()
udp_port = 12345
SIZE = 4096
print ("UDP target IP:", udp_host)
print ("UDP target Port:", udp_port)
file_name = input("Please Enter the File Name : ")
sock.sendto(bytes("FILESENDING","utf-8"),(udp_host,udp_port))
sock.sendto(bytes(file_name,"utf-8"),(udp_host,udp_port))
file = open("files_folder/"+file_name,"rb")
data = file.read(SIZE)
while data:
    sock.sendto(data,(udp_host,udp_port))
    data = file.read(SIZE)
    print(data)
file.close()
print("data send from the client")

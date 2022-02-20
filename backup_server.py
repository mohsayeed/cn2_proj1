import struct
import random
import socket

prev_frame_num = 0

def receiver_checksum_crc(data_in):
    polynomial_value = 0xB9B1
    size = len(data_in)
    result = 0
    for i in range(0,size):
        byte = (data_in[i])                #convert byte to binary
        for j in range(0,8):                        #
            if(not  ((result & 1) ^ (byte & 1))):        #
                result >>= 1
            elif((result & 1) ^ (byte & 1)):
                result = (result >> 1) ^ polynomial_value 
            byte >>= 1                        #
    return result                              #return answer

def random_errordec(result_checksum): 
    random_value = random.randint(0,3) 
    if random_value != 2:
        return result_checksum
    elif(random_value==2):
        return result_checksum%2

def data_check( frame_in_num , data, checksum_client ):
    global prev_frame_num
    checksum_server = random_errordec(receiver_checksum_crc(data))
    if frame_in_num != prev_frame_num + 1 or checksum_client != checksum_server :
        return 0
    elif(frame_in_num == prev_frame_num + 1 and checksum_client == checksum_server):
        prev_frame_num += 1                    
        return 1

def startserver():
    ack = struct.Struct('I I') 
    frame = struct.Struct('I I 8s I')
    curr_frame_num = 1
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udp_host = socket.gethostname()	
    udp_port = 12345 
    serverSocket.bind((udp_host,udp_port))
    print ('Server is up and running')
    data = serverSocket.recvfrom(1024)
    addresspair = data[1]
    file_name = data[0].decode('utf-8')
    file = open(("received"+file_name), "wb")
    while True:                                         #loop while boolean flag is true
        if prev_frame_num == curr_frame_num:                #update expexted frame number
            curr_frame_num += 1
        data_packed = serverSocket.recvfrom(1024)           #recieve data
        data_packed = data_packed[0]
        print(data_packed)
        if len(data_packed)>0:
            frame_in_num, frame_insize, data, checksum_client = frame.unpack(data_packed)   #unpack data
            # print(frame_in_num, data_packed)
            frame_out_ack = data_check(frame_in_num, data, checksum_client)             #verify frame in, and decide output ack
            if frame_out_ack == 1:                          #
                file.write(data)            #if frame was valid, write to file
            frame_out = ack.pack(curr_frame_num, frame_out_ack)     #pack ack frame
            serverSocket.sendto(frame_out,(addresspair))                    #send ack frame
        if data == b'\x00\x00\x00\x00\x00\x00\x00\x00':  #check for empty frame, to signify end
            break

    serverSocket.close()                                #close socket
    file.close()                                            #close file
startserver()
import struct as strct
import random
import socket
import os
import math 

def cyclic_redundancy_check(data_in):
    result = 0 
    size = len(data_in)
    polynomial = 0xB9B1 
    for i in range(0,size):
        byte = (data_in[i])
        for j in range(0,8):                        
            if not ((result & 1) ^ (byte & 1)): 
                result >>= 1 
            elif((result & 1) ^ (byte & 1)):
                result = (result >> 1) ^ polynomial                  
            byte >>= 1 
    return result
def random_errordec(result_checksum): 
    random_value = random.randint(0,3) 
    if random_value != 2:
        return result_checksum
    elif(random_value==2):
        return result_checksum%2



def main():
    file = open("sample_data.txt", "rb")
    file_size = os.stat('sample_data.txt')
    final_frames = (math.ceil(file_size.st_size/8))
    frame = strct.Struct('I I 8s I') 
    ack = strct.Struct('I I') 
    frame_number = 1 
    udp_host = socket.gethostname()
    udp_port = 12345 
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    clientSocket.sendto((bytes("sample_data.txt","utf-8")),(udp_host,udp_port))
    while frame_number<=final_frames:
        data = file.read(8) 
        if data == "":
            break
        checksum = random_errordec(cyclic_redundancy_check(data))
        values = (frame_number, frame.size, data, checksum)
        frame_out = frame.pack(*values)             #pack data in frame
        clientSocket.sendto(frame_out,(udp_host,udp_port))
        if data == b'\x00\x00\x00\x00\x00\x00\x00\x00':
            break
        data_packed = clientSocket.recvfrom(1024)
        data_packed = data_packed[0]
        frame_in_num, frame_in_ack = ack.unpack(data_packed) 
        while frame_in_ack == 0: 
            print('To Server:', frame_number, frame_out)
            print('From Server:', frame_in_num, 'ack =', frame_in_ack)
            checksum = cyclic_redundancy_check(data) 
            checksum = random_errordec(checksum)
            values = (frame_number, frame.size, data, checksum)
            frame_out = frame.pack(*values)
            clientSocket.sendto(frame_out,(udp_host,udp_port))
            data_packed = clientSocket.recvfrom(1024)
            data_packed = data_packed[0]
            frame_in_num, frame_in_ack = ack.unpack(data_packed)
        if frame_in_num == frame_number and frame_in_ack == 1:
            frame_number += 1
            if(frame_number==final_frames):
                values = (frame_number, frame.size, b'\x00\x00\x00\x00\x00\x00\x00\x00', checksum)
                frame_out = frame.pack(*values)
                clientSocket.sendto(frame_out,(udp_host,udp_port))
                break

    clientSocket.close()

main()
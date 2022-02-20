import struct
import random
import socket
import os
import math 

#CRC function
def crc16(data_in):
    # data_in= data_in.decode("utf-8")
    print(type(data_in),len(data_in))
    poly = 0xB9B1                           #We use a polynomial of 0xB9B1
    size = len(data_in)                     #find the size of the data in, for loop
    crc = 0                                 #initalise remainder
    i = 0                                   #position in data
    while i < size:                         #loop through data
        byte = (data_in[i])                #convert byte to binary
        j = 0                               #loop through byte
        while j < 8:                        #
            if (crc & 1) ^ (byte & 1):        #
                crc = (crc >> 1) ^ poly     #divide by polynomial
            else:
                crc >>= 1                   #shift bit into remainder
            byte >>= 1                        #
            j += 1
        i += 1
    return crc                              #return answer

def gremlin_func(crc_in):                   #gremlin function
    i = random.randint(0,3)                 #choose a random number between 0 and 3
    if i == 2:                              #if random nuber is 2
        return crc_in % 2                   #get modulus 2 of crc. Modulus was chosen,
                                            #as answer guarentted to be in correct range
    else:
        return crc_in

file = open("sample_data.txt", "rb")         #open text file, in read mode
file_size = os.stat('sample_data.txt')
final_frames = (math.ceil(file_size.st_size/8))
frame = struct.Struct('2I 8s I')            #struct template for frame out
ack = struct.Struct('2I')                   #struct for ack frame
frame_number = 1                            #current frame number
end = 0

udp_host = socket.gethostname()
udp_port = 12345                            #port 12000
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)     #create a socket
clientSocket.sendto((bytes("sample_data.txt","utf-8")),(udp_host,udp_port))

while end == 0:                                 #while boolean flag end is true
    #get data
    data = file.read(8)                         #read in 8 bytes from file
    if data == "":                              #if data is empty, end
        end = 1
    #get checksum
    checksum_pre_gremlin = crc16(data)          #get checksum
    checksum = gremlin_func(checksum_pre_gremlin)#gremlin checksum

    #pack and send data
    values = (frame_number, frame.size, data, checksum)
    frame_out = frame.pack(*values)             #pack data in frame
    clientSocket.sendto(frame_out,(udp_host,udp_port))
    if data == b'\x00\x00\x00\x00\x00\x00\x00\x00':
        end = 1
        break
    data_packed = clientSocket.recvfrom(1024)       #reciever data
    data_packed = data_packed[0]
    frame_in_num, frame_in_ack = ack.unpack(data_packed)       #unpack sata

    print('To Server:', frame_number, frame_out)
    print('From Server:', frame_in_num, 'ack =', frame_in_ack)

    #if nak
    while frame_in_ack == 0:                    #while wrong frame
        print('To Server:', frame_number, frame_out)
        print('From Server:', frame_in_num, 'ack =', frame_in_ack)

        #new checksum (for gremlin)
        checksum = crc16(data)      #gennerate new checksum
        checksum = gremlin_func(checksum)   #gremlin new checksum
        values = (frame_number, frame.size, data, checksum)
        frame_out = frame.pack(*values)
        clientSocket.sendto(frame_out,(udp_host,udp_port))            #send new frame

        #receive ack
        data_packed = clientSocket.recvfrom(1024)
        data_packed = data_packed[0]
        frame_in_num, frame_in_ack = ack.unpack(data_packed)

    #make sure ack and correct frame
    if frame_in_num == frame_number and frame_in_ack == 1:  #update frame number
        frame_number += 1
        if(frame_number==final_frames):
            values = (frame_number, frame.size, b'\x00\x00\x00\x00\x00\x00\x00\x00', checksum)
            frame_out = frame.pack(*values)             #pack data in frame
            clientSocket.sendto(frame_out,(udp_host,udp_port))
            end = 1


clientSocket.close()        #close socket


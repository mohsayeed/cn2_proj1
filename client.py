#!usr/bin/python

import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udp_host = socket.gethostname()
udp_port = 12345
SIZE = 4096
msg = "Hello Python!"
print ("UDP target IP:", udp_host)
print ("UDP target Port:", udp_port)
sock.sendto(bytes(msg,"utf-8"),(udp_host,udp_port))
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


# import socket
# import sys
# import threading
# import tkinter

# clientSocket_1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# clientName = input("Please enter your Name : ")
# clientSocket_1.send(bytes(clientName,"utf-8"))
# print("Transfering you to Chat Room....")
# SIZE=1024
# Send_string = "FILESEND"

# def receiveMsg ( msgList ):

# 	while True:
# 		message = clientSocket_1.recv(1024)
# 		message = message.decode("utf-8")

# 		if ( message.find("ACTIVE MEMBERS") != -1 ):
# 			msgList.insert(tkinter.END,message)

# 		elif ( message.find("has been added to the Chat") != -1 ):
# 			msgList.insert(tkinter.END,'                                {}'.format(message))

# 		elif (message.find(Send_string)!=-1):
# 			msgList.insert(tkinter.END,'                                                                {}'.format(message))
# 			x = message.split(" ")
# 			file = open(("client1/"+x[1]),"wb")
			
# 			data = clientSocket_1.recv(SIZE)
# 			file.write(data)
# 			while (len(data) >= SIZE ):
# 				data = clientSocket_1.recv(SIZE)
# 				file.write(data)
# 			file.close()

# 		else:
# 			msgList.insert(tkinter.END,'                                                                {}'.format(message))


# def sendMsg ( textInput, msgList, clientSocket_1 ):

# 	req = textInput.get()
# 	textInput.delete(0, tkinter.END)

# 	msgList.insert(tkinter.END,"You : " + req)

# 	if ( req.find("QUIT") != -1 ):
# 		clientSocket_1.send(bytes(req,"utf-8"))
# 		msgList.insert(tkinter.END,'You have left the chat')
# 		sys.exit()

# 	elif (req.count("FILESEND")>0):
# 		clientSocket_1.send(bytes(req,"utf-8"))
# 		x = req.split(" ")
# 		file = open("data/"+x[1],"rb")
# 		data = file.read(SIZE)
# 		while data:
# 			clientSocket_1.send(data)
# 			data = file.read(SIZE)
# 		file.close()

# 	else:
# 		clientSocket_1.send(bytes(req,"utf-8"))


# chatWindow = tkinter.Tk()
# chatWindow.title('Chatroom')

# frameMsgs = tkinter.Frame(master=chatWindow)
# scrollBar = tkinter.Scrollbar(master=frameMsgs)

# msgList = tkinter.Listbox (
#     master=frameMsgs, 
#     yscrollcommand=scrollBar.set
# )

# scrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y, expand=False)
# msgList.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

# frameMsgs.grid(row=0, column=0, columnspan=5, sticky="nsew")

# frameEntry = tkinter.Frame(master=chatWindow)
# textInput = tkinter.Entry(master=frameEntry)
# textInput.pack(fill=tkinter.BOTH, expand=True)

# textInput.bind("<Return>", lambda x: sendMsg(textInput, msgList, clientSocket_1) )
# textInput.insert(0, "Please enter your message here")

# sendButton = tkinter.Button(
#     master=chatWindow,
#     text='send',
#     command=lambda: sendMsg(textInput, msgList, clientSocket_1)
# )

# frameEntry.grid(row=1, column=0, padx=10, sticky="ew")
# sendButton.grid(row=1, column=1, pady=10, sticky="ew")

# chatWindow.rowconfigure(0, minsize=500, weight=1)
# chatWindow.rowconfigure(1, minsize=50, weight=0)
# chatWindow.columnconfigure(0, minsize=500, weight=1)
# chatWindow.columnconfigure(1, minsize=200, weight=0)


# recvThread = threading.Thread(target=receiveMsg, args=(msgList,))
# recvThread.daemon = True
# recvThread.start()

# msgList.insert(tkinter.END,"                Welcome to the Chat Room !!")

# chatWindow.mainloop()
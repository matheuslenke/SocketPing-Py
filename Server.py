from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server is ready to receive")
print("Press CTRL + C if you want to exit")

while True:
    message, clientAddress = serverSocket.recvfrom(2048)

    modifiedMessage = message.decode().upper()
    print("Received message")
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
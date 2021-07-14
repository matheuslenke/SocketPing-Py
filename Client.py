import socket
import sys
from timeit import default_timer as timer

def sendMessage(message):
    clientSocket.sendto(message, (serverName, serverPort))

def receiveMessage():
    receivedMessage, serverAddress = clientSocket.recvfrom(2048)
    strippedMessage = receivedMessage.decode('utf-8').strip()
    if len(strippedMessage) <= 30:
        print(strippedMessage)

# Getting arguments
if len(sys.argv) == 3:
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])
else:
    print("Wrong usage. Correct form: python3 Client.py <serverIp> <port>")
    exit(1)

# Specifying Socket to UDP
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM  )

message = input('Input lowercase sentence:')
encodedMessage = message.encode('utf-8')
# Sending 10 pings
for x in range(10):
    start = timer()
    sendMessage(encodedMessage)
    receiveMessage()
    end = timer()
    print((end - start) * 1000)

clientSocket.close()
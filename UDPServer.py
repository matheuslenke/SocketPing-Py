from socket import *

# What's your IP address and witch port should we use?
recieve_host = '127.0.0.1'
recieve_port = 30000

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind((recieve_host, recieve_port))


while True:
  message, address = serverSocket.recvfrom(50)
  decodedList = list(message.decode('utf-8'))
  decodedList[5] = "1"
  finalMessage = "".join(decodedList)
  print ('Recieve: ' + message.decode('utf-8'))
  serverSocket.sendto(finalMessage.encode('utf-8'), address)
 
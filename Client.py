from os import times
import socket
import sys
import time
import datetime

sockets = []

# Functions
def TimestampMillisec64():
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)

def sendMessage(message):
    clientSocket.sendto(message, (serverName, serverPort))

def receiveMessage(x):
    receivedMessage, serverAddress = clientSocket.recvfrom(50)
    decodedMessage = receivedMessage.decode('utf-8')

    # Checking if message is valid
    sequenceCode = decodedMessage[:5]
    typeIdentifier = decodedMessage[5]
    timestamp = decodedMessage[6:10]
    stringSent = decodedMessage[10:]
    print(sequenceCode, typeIdentifier, timestamp, stringSent)

    if len(decodedMessage) > 40:
        print("Socket does not conform to protocol")
        return None
    if typeIdentifier != "1":
        print("Socket does not conform to protocol")
        return None
    print(decodedMessage)
    return decodedMessage

# Getting arguments
if len(sys.argv) == 3:
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])
else:
    print("Wrong usage. Correct form: python3 Client.py <serverIp> <port>")
    exit(1)

# Specifying Socket to UDP
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM  )
clientSocket.settimeout(5)


# Main logic: Sending 10 pings
for x in range(10):
    try:
        start = datetime.datetime.now()
        startms = TimestampMillisec64()
        message = bytes(f'{x:05d}0{str(start.microsecond)[-4:]}Matheus Lenke Coutinho________', 'utf-8')
        sockets.append((x, startms, message))
        sendMessage(message)
        time.sleep(0.5)
        receiveMessage(x)

        end = datetime.datetime.now()
        print(f'Socket {x:05d} rtt: {int((end - start).total_seconds() * 1000)}ms')
    except socket.timeout as e:
        print(f'Socket {x:05d} error: {e}')
        continue

# print(sockets)
clientSocket.close()

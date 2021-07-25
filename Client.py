from math import sqrt
from os import times
import socket
import sys
import time
import datetime

sockets = [] # Armazenamento dos dados do socket
totalSocketsTransmitted = 0 # Contador de Sockets transmitidos
totalSocketsToTransmit = 10 # Total de sockets a serem enviados

# Função para pegar Timestamp em ms
def TimestampMillisec64(timeToCalculate):
    return int(str(int((timeToCalculate - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)))

# Função de envio de mensagem
def sendMessage(message):
    clientSocket.sendto(message, (serverName, serverPort))

# Função com a lógica de receber mensagem
def receiveMessage(x):
    receivedMessage, serverAddress = clientSocket.recvfrom(50)
    decodedMessage = receivedMessage.decode('utf-8')

    # Pegando informações da mensagem recebida
    sequenceCode = decodedMessage[:5]
    typeIdentifier = decodedMessage[5]
    timestamp = decodedMessage[6:10]
    stringSent = decodedMessage[10:]

    # Mensagem com tamanho errado
    if len(decodedMessage) > 40:
        print(f'Socket {sequenceCode} does not conform to protocol')
        return None
    # Mensagem não retornou Pong
    if typeIdentifier != "1":
        print(f'Socket {sequenceCode} does not conform to protocol')
        return None

    # Verifica se o socket recebido existe
    socket = sockets[int(sequenceCode)]
    if socket == None:
        print(f'Socket {sequenceCode} does not conform to protocol')
        return None
    # Atualiza socket recebido e retorna
    socket['returned'] = True
    sequence = int(sequenceCode)
    return (decodedMessage, timestamp, stringSent, sequence)

# # Getting arguments
# if len(sys.argv) == 3:
#     serverName = sys.argv[1]
#     serverPort = int(sys.argv[2])
# else:
#     print("Wrong usage. Correct form: python3 Client.py <serverIp> <port>")
#     exit(1)

serverName = '127.0.0.1'
serverPort = 30000

# Specifying Socket to UDP
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM  )
clientSocket.settimeout(1)
socketsStartTransmitting = datetime.datetime.now()

# Main logic: Sending 10 pings
for x in range(totalSocketsToTransmit):
    try:
        # Construindo a mensagem
        start = datetime.datetime.utcnow()
        # Pegando milissegundos
        start2 = TimestampMillisec64(start)
        id = f'{x:05d}'
        # Pegando 4 dígitos do Timestamp
        startTimestamp = str(start2)[-4:]
        message = bytes(f'{x:05d}0{startTimestamp}Matheus Lenke Coutinho________', 'utf-8')
        # Armazena dados do Socket em um Dictionary
        sockets.append({
            "id": id,
            "startTime": startTimestamp,
            "message": message,
            "returned": False,
            "endTime": None,
            'totalMs': 0,
        })
        
        # Envia a mensagem
        sendMessage(message)
        totalSocketsTransmitted += 1
        # Aguarda a mensagem e realiza validações
        (receivedMessage, receivedTimestamp, receivedString, sequence) = receiveMessage(x)
        if receivedMessage == None:
            continue

        # Calculando timestamp final
        end = datetime.datetime.utcnow()
        end2 = TimestampMillisec64(end)
        endTimestamp = str(end2)[-4:]
        
        # Calculo do Timestamp e armazenamento
        if endTimestamp >= receivedTimestamp:
            totalTime = (int(endTimestamp) - int(receivedTimestamp))
        else:
            totalTime = (int(endTimestamp) - 10000 + int(receivedTimestamp))
        sockets[sequence]['totalMs'] = totalTime
        sockets[sequence]['endTime'] = endTimestamp

        # Imprimindo relatório final para Socket recebido
        print(f'Socket {sequence} rtt: {totalTime}ms start: {startTimestamp} end: {endTimestamp}')
    except socket.timeout as e:
        # Imprime se socket deu timeout
        print(f'Socket {sequence} error: {e}')
        continue

clientSocket.close()

# Calcula tempo total da operação
socketsEndTransmitting = datetime.datetime.now()
socketsTotalTime = int((socketsEndTransmitting - socketsStartTransmitting).total_seconds() * 1000)

#  ------ Cálculos Finais ------
totalSocketsReturned = 0
rttMin = 100000
rttMax = 0
totalRtt = 0

# Calculando a média de rtt
for item in sockets:
    if item['returned'] == True:
        totalSocketsReturned += 1
        totalRtt += item['totalMs']
        if item['totalMs'] < rttMin:
            rttMin = item['totalMs']
        if item['totalMs'] > rttMax:
            rttMax = item['totalMs']
averageRtt = totalRtt / totalSocketsReturned

# Calculando desvio padrão
mdevSum = 0
for item in sockets:
    if item['returned'] == True:
        difference = item['totalMs'] - averageRtt
        mdevSum += pow(difference, 2)
mdev = sqrt(mdevSum / totalSocketsTransmitted) 

# Imprimindo relatório final
packetLoss = int(((totalSocketsToTransmit - totalSocketsReturned) / totalSocketsTransmitted) * 100)
print(f'{totalSocketsTransmitted} packets transmitted, {totalSocketsReturned} received, {packetLoss}% packet loss, time: {socketsTotalTime}ms')
print(f'rtt min/avg/max/mdev = {rttMin}/{averageRtt}/{rttMax}/{round(mdev,3)}')


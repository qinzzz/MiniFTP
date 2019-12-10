#client
import socket
ip_port = ('127.0.0.1', 21)
buffersize = 1024

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect(ip_port)
try:
    while True:
        data = input('>>>')
        socket_client.send(data.encode('utf-8'))
        if not data: continue
        if data == 'bye':
            break
        length = socket_client.recv(buffersize)
        length = int(length.decode('gbk'))
        socket_client.send('ready'.encode("gbk"))
        response = b''
        while len(response) < length:
            response += socket_client.recv(buffersize)
        print(response.decode('gbk'))
except Exception as e:
    print(e)
    print('connect close')
    socket_client.close()
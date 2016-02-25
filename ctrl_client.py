import socket

HOST = '127.0.0.1'
PORT = 9999
def ctrl_client(addr, data):
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, 
                          _sock=None)
    client.connect(addr)
    client.send(data)
   # response = client.recv(1024)
    response = ""
    while True:
        ret = client.recv(1024)
        if ret == '':
            break
        response = response + ret
    print response
    client.close()
    
    
ctrl_client((HOST, PORT), "process get all")
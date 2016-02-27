import socket
import time
"""
s = socket.socket()
s.connect(('127.0.0.1', 28878))
s.send('service get_running_service')
response = ""
while True:
    ret = s.recv(1024)
    if ret == "":
        break
    response = response + ret
    
print response
s.close()
#time.sleep(0)
"""
s = socket.socket()
s.connect(("127.0.0.1", 9999))
s.send('# ipconfig')
response = ""
while True:
    ret = s.recv(1024)
    if ret == "":
        break
    response = response + ret
    
print response
s.close()

del s
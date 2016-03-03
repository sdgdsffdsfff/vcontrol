#import os
import threading
import time
import socket

"""
cmd = 'powershell ".\\vprocess.ps1 -get-processbyname *"'
data = os.popen(cmd).read()
print data
"""
class process_info(threading.Thread):
    def __init__(self, process_num = 0, name = 'target_process_info', update_time = 5, target_addr = None) :
        threading.Thread.__init__(self, name = name)
        
        self.process_num = process_num
        self.process_items = []
        self.keys = []
        self.is_working = False
        self.raw_data = None
        self.update_time = update_time
        self.target_addr = target_addr
        self.update_cmd = "process get all"
        
    def run(self):
        """This func is keep the process_info update"""
        if self.is_working == False:
            self.is_working = True
        else:
            pass
        
        while self.is_working:
            if self.process_items != []:
                self.process_items = []
            #time.sleep(self.update_time)
            self.update()
            for i in self.process_items:
                print i
            time.sleep(self.update_time)
            
    
    def stop(self):
        if self.is_working == True:
            self.is_working = False
        else :
            pass
        
    
    def create(self, value = []):
        if self.keys == []:
            print "[!] Empty Keys!"
            return 0
        if value == []:
            print "[!] Empty Values!"
            return 0
        
        process_item = {}
        for i in range(len(self.keys)):
            process_item[self.keys[i]] = value[i]

        
        if process_item != {}:
            self.process_items.append(process_item)
            
        self.process_num = self.process_num + 1
        return 1
        
    def update(self):
        self.request_info()
        self.analyze()
        

    def request_info(self):
        s = socket.socket()
        s.connect(self.target_addr)
        s.send(self.update_cmd)
        response = ""
        while True:
            ret = s.recv(1024)
            if ret == "":
                print "[^] Data End"
                break
            response = response + ret
        print "[^] Debug I/O"
        #print response
        
        self.raw_data = response
        
        s.close()
        
    def analyze(self):
        data_list = self.raw_data.splitlines()
        self.keys = data_list[1].split()
        for i in range(len(data_list) - 3):
            ret = i + 3
            tmp = data_list[ret].split()
            if len(tmp) == len(self.keys) - 1:
                tmp.insert(5,'N/A')
            else:
                pass
            self.create(tmp)
"""
data_list = data.split("\n")
for i in data_list:
    i.strip()
    if i == "":
        continue
    print "---------------------------------------------------"
    print i

item = data_list[1].split()
print item
processes = multi_process_info(key=item)
for i in range(len(data_list)-3):
    ret = i + 3
    tmp = data_list[ret].split()
    print tmp
    if len(tmp) == len(item)-1:
        tmp.insert(5,'0.00')
    processes.create(tmp)
    
for i in processes.process_items:
    print i
"""


if __name__ == "__main__":
    print "Prepare!"
    info1 = process_info(process_num=0, name='target_process_info', 
                        update_time=5, 
                        target_addr=("127.0.0.1",9999))
    info1.start()

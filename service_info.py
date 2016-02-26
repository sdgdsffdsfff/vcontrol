import threading
import socket
import time
import os


#cmd = 'powershell ".\\vservice.ps1 -get-runningservice"'
#data = os.popen(cmd).read()
#print data

class service_info(threading.Thread):
    def __init__(self, name = 'target_service_info', update_time = 5, target_addr = None) :
        threading.Thread.__init__(self, name = name)
        
        self.running_service_num = 0
        self.stopped_service_num = 0
        
        self.running_service_items = []
        self.stopped_service_items = []
        self.keys = []
        
        self.is_working = False
        
        #raw_data
        self.running_service_raw_data = ""
        self.stopped_service_raw_data = ""
        self.update_time = update_time
        self.target_addr = target_addr
        
        #ctrl_cmd
        self.update_running_service_cmd = "service get_running_service"
        self.update_stopped_service_cmd = "service get_stopped_service"
        
    def run(self):
        if self.is_working == False:
            self.is_working = True
        else:
            pass
        
        while self.is_working:
            #time.sleep(self.update_time)
            self.update()
            time.sleep(self.update_time)
    
    def stop(self):
        if self.is_working == True:
            self.is_working = False
        else :
            pass
        
    
    def create(self, value = [], is_running_service = True):
        if self.keys == []:
            print "[!] Empty Keys!"
            return 0
        if value == []:
            print "[!] Empty Values!"
            return 0
        
        service_item = {}
        for i in range(len(self.keys)):
            service_item[self.keys[i]] = value[i]

        
        if service_item != {}:
            if is_running_service == True:
                self.running_service_items.append(service_item)
                self.running_service_num = self.running_service_num + 1
            else:
                self.stopped_service_items.append(service_item)
                self.running_service_num = self.stopped_service_num + 1
            
        #self.process_num = self.process_num + 1
        return 1
        
    def update(self):
        self.request_info()
        self.analyze()
        

    def request_info(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.target_addr)
        #update running service
        s.send(self.update_running_service_cmd)
        response = ""
        while True:
            ret = s.recv(1024)
            if ret == "":
                print "[^] Data End"
                break
            response = response + ret
        print "[^] Debug I/O"
        print response        
        self.running_service_raw_data = response
        s.close()
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #update stopped services
        s.connect(self.target_addr)
        s.send(self.update_stopped_service_cmd)
        while True:
            ret = s.recv(1024)
            if ret == "":
                print "[^] Data End"
                break
            response = response + ret
        self.stopped_service_raw_data = response
        s.close()
        
    def analyze(self):
        data_list = self.running_service_raw_data.splitlines()
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
    info1 = service_info(
                        update_time=5, 
                        target_addr=("127.0.0.1",28878))
    info1.start()

import socket

class control:
    """This class can control target £º close & start service£¬ kill or start process and get a shell"""
    def __init__(target_addr = None):
        self.target_addr = target_addr
        
        self.stop_service_cmd = "service stop "
        self.start_service_cmd = 'service start '
        self.kill_process_cmd = 'process kill '
        
        self.raw_cmd = 'raw '
        self.feedback = ""
    def __init_field__(self):
        
        self.stop_service_cmd = "service stop "
        self.start_service_cmd = 'service start '
        self.kill_process_cmd = 'process kill '
        
        self.raw_cmd = 'raw '        
    def kill_process(self, process_name = ""):
        self.__init_field__()
        self.kill_process_cmd = self.kill_process_cmd + process_name
        self.send_cmd(self.kill_process_cmd)
        
    def stop_service(self, service_name = ""):
        self.__init_field__()
        self.stop_service_cmd = self.stop_service_cmd + service_name
        self.send_cmd(self.stop_service_cmd)
        
    def start_service(self, service_name = ""):
        self.__init_field__()
        self.start_service_cmd = self.start_service_cmd + service_name
        self.send_cmd(self.start_service_cmd)
        
    def raw_cmd(self, cmd = ""):
        self.__init_field__()
        self.raw_cmd = self.raw_cmd + cmd
        self.send_cmd(self.raw_cmd)
        
    def send_cmd(self, cmd):
        if self.feedback != "":
            self.feedback = ""
        
        s = socket.socket()
        s.connect(self.target_addr)
        s.send(cmd)
        response = 0
        while True:
            ret = s.recv(1024)
            if ret == "":
                print "[!] Empty FeedBack"
                break
            response = response + ret
        print response
        self.feedback = response
        s.close()
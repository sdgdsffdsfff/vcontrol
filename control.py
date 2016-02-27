#encoding:utf-8
import socket

class control:
    """This class can control target ： close & start service， kill or start process and get a shell"""
    def __init__(self, target_addr = ("127.0.0.1", 28878)):
        self.target_addr = target_addr
        
        self.stop_service_cmd = "service stop "
        self.start_service_cmd = 'service start '
        self.kill_process_cmd = 'process kill '
        
        self.raw_cmd = '# '
        self.feedback = ""
    def __init_field__(self):
        
        self.stop_service_cmd = "service stop "
        self.start_service_cmd = 'service start '
        self.kill_process_cmd = 'process kill '
        
        self.raw_cmd = '# '        
    def kill_process(self, process_name = ""):
        self.__init_field__()
        self.kill_process_cmd = self.kill_process_cmd + process_name
        self.__send_cmd(self.kill_process_cmd)
        
    def stop_service(self, service_name = ""):
        self.__init_field__()
        self.stop_service_cmd = self.stop_service_cmd + service_name
        self.__send_cmd(self.stop_service_cmd)
        
    def start_service(self, service_name = ""):
        self.__init_field__()
        self.start_service_cmd = self.start_service_cmd + service_name
        self.__send_cmd(self.start_service_cmd)
        
    def send_raw_cmd(self, cmd = ""):
        self.__init_field__()
        self.raw_cmd = self.raw_cmd + cmd
        self.__send_cmd(self.raw_cmd)
        
    def __send_cmd(self, cmd):
        if self.feedback != "":
            self.feedback = ""
        
        s = socket.socket()
        s.connect(self.target_addr)
        s.send(cmd)
        response = ""
        while True:
            ret = s.recv(1024)
            if ret == "":
                print "[!] Empty FeedBack"
                break
            response = response + ret
        print response
        self.feedback = response
        s.close()
        

controler = control(target_addr = ("127.0.0.1", 9999))
controler.send_raw_cmd(cmd='ipconfig')
controler.kill_process(process_name="360se")
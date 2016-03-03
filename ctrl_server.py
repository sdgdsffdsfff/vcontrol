#encoding:utf-8
import SocketServer
import os
import threading
import time
import bs4

class ctrl_server(SocketServer.ThreadingTCPServer):
    pass

class ctrl_handler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.html_data = ""
        self.sys_cmd = "powershell "
        self.soup = None        
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        try:
            cmd = self.request.recv(1024)
        except:
            error_data = '[!] Error ! Receive Failed!'
            print error_data
            self.request.send(error_data)
            raise
        print cmd
        
        if cmd.startswith('#'):
            self.sys_cmd = cmd[2:]
            self.execute_raw(self.sys_cmd)
        else:    
            self.execute(cmd)

    def execute_raw(self, cmd):
        response = os.popen(cmd).read()
        self.request.send(response)
        self.request.close()
        
    def execute(self, cmd = ""):
        self.parse(cmd)
        try:
            self.html_data = os.popen(self.sys_cmd).read()
            print self.html_data
            self.request.send(self.html_data)
            self.request.close()
        except:
            raise

  
        
    def parse(self, cmd = ""):
        """This func is to parse cmd from remote server"""
        cmd_list = cmd.split(" ")
        script_name = cmd_list[0]
        
        if script_name == 'process':
            self.sys_cmd = self.sys_cmd + '".\\vprocess.ps1'
            if cmd_list[1] == 'get':
                self.sys_cmd = self.sys_cmd + ' -get-processbyname'
                try:
                    if cmd_list[2] == 'all':
                        self.sys_cmd = self.sys_cmd + ' *'
                    else:
                        self.sys_cmd = self.sys_cmd + ' *' + cmd_list[2] + '*'
                except:
                    print "[!] bad cmd"
                    return 0
            elif cmd_list[1] == 'kill':
                self.sys_cmd = self.sys_cmd + ' -kill-byname'
                try:
                    self.sys_cmd = self.sys_cmd + ' ' + cmd_list[2]
                except:
                    print "[!] bad cmd"
                    return 0
            elif cmd_list[1] == 'count':
                self.sys_cmd = self.sys_cmd + ' -get-count'
                pass
            else:
                pass
            
        elif script_name == 'service':
            self.sys_cmd = self.sys_cmd + '".\\vservice.ps1'
            if cmd_list[1] == 'get':
                try:
                    if cmd_list[2] == 'all':
                        self.sys_cmd = self.sys_cmd + ' *'    
                    else:
                        self.sys_cmd = self.sys_cmd + ' *' + cmd_list[2] + '*'
                except:
                    return 0
            elif cmd_list[1] == 'get_running_service':
                self.sys_cmd = self.sys_cmd + ' -get-runningservice'
            elif cmd_list[1] == 'get_stopped_service':
                self.sys_cmd = self.sys_cmd + ' -get-stoppedservice'
            elif cmd_list[1] == 'start':
                self.sys_cmd = self.sys_cmd + ' -start-servicebyname'
                try:
                    if cmd_list[2] == 'all':
                        self.sys_cmd = self.sys_cmd + ' *'    
                    else:
                        self.sys_cmd = self.sys_cmd + cmd_list[2]                 
                except:
                    return 0
            elif cmd_list[1] == 'stop':
                self.sys_cmd = self.sys_cmd + ' -stop-servicebyname'
                try:
                    if cmd_list[2] == 'all':
                        self.sys_cmd = self.sys_cmd + ' *'    
                    else:
                        self.sys_cmd = self.sys_cmd + cmd_list[2]                 
                except:
                    return 0                
            else:
                print "[!] Failed！"
                return 0            
        elif script_name == 'pc_info':
            self.sys_cmd = self.sys_cmd + ' ".\\vpcinfo.ps1'
            if cmd_list[1] == 'bios':
                self.sys_cmd = self.sys_cmd + ' -bios"'
            elif cmd_list[1] == 'desktop':
                self.sys_cmd = self.sys_cmd + ' -desktop"'
            elif cmd_list[1] == 'sysinfo':
                self.sys_cmd = self.sys_cmd + ' -sysinfo"'
            elif cmd_list[1] == 'cpu':
                self.sys_cmd = self.sys_cmd + ' -cpu'
            elif cmd_list[1] == 'harddisk':
                self.sys_cmd = self.sys_cmd + ' -harddisk'
            elif cmd_list[1] == 'time':
                self.sys_cmd = self.sys_cmd + ' -time'
            else:
                print "[!] cmd_option fail"
                return 0
        else:
            print "[!] Error!"
            return 0
        self.sys_cmd = self.sys_cmd + "\""
        print self.sys_cmd
        return 1
        
                
HOST = '127.0.0.1'
PORT = 9999
server = ctrl_server((HOST, PORT), ctrl_handler)
server.serve_forever()
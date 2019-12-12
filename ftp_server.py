# server
import os
import sys
import time
import socket
import subprocess
import threading
from utils import removeDir

try:
    HOST = socket.gethostbyname(socket.gethostname( ))
except socket.gaierror:
    HOST = '127.0.0.1'
PORT = 21
BUFSIZE = 1024
LOCALDIR = '/Users/qinzzz/ftp'


class MiniFTP(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.cwd = LOCALDIR
        self.conn = conn
        self.serverAddr = addr
        self.dataConn = None
        self.passive_on = False
        self.mode = 'I'
        self.sendCmd('220 ---- Welcome to Portal of MiniFTP ---- \r\n')
        

        
    def run(self):
        while True:
            try:
                data = self.conn.recv(BUFSIZE).rstrip()
                try:
                    cmd = data.decode('utf-8')
                except AttributeError:
                    cmd = data
                self.log('Receive', cmd)
                
            except socket.error as err:
                self.log('Receive error', err)

            try:
                if not cmd:
                    break
                else:
                # cmd, arg = cmd[:4].strip(), cmd[4:].strip( ) or None
                    command = cmd.split()[0]
                    arg = cmd.split()[1:]
                    arg = ' '.join(arg)
                    func = getattr(self, command)
                    if func:
                        func(arg)
                    else:
                        self.log(command, 'Unknown command.')
            except AttributeError as err:
                self.sendCmd('500 Syntax error, command unrecognized.\r\n')
                self.log('Receive', err)
  

    def USER(self, user):
        self.log("USER", user)
        if not user:
            self.sendCmd('501 Syntax error in parameters or arguments.\r\n')

        else:
            self.sendCmd('331 Enter password.\r\n')
            self.username = user


    def PASS(self, passwd): 
        self.log("PASS", passwd) 
        if not passwd:
            self.sendCmd('501 Syntax error in parameters or arguments.\r\n')

        elif not self.username:
            self.sendCmd('503 Bad sequence of commands.\r\n')

        else:
            # self.sendCmd('230 User logged in, proceed.\r\n')
            self.passwd = passwd
            self.authenticated = self.loginAuth()
            if not self.authenticated:
                self.conn.close()
            # else:
            #     self.PASV()


    # TODO：修改明文传输密码
    '''
        Check login authority. 
        Save user information in 'auth.config' as 
            username password \n

    '''
    def loginAuth(self):
        f = open('auth.config', 'r')
        for line in f.readlines():
            user, pswd = line.split()
            if user == self.username and pswd == self.passwd:
                self.log("Login", "success")
                self.sendCmd("230 User logged in as %s \r\n" %(user))
                return True
        self.sendCmd('530 Login incorrect.\r\n')
        return False

    # quit FTP service
    def QUIT(self, cmd):
        self.sendCmd('221 Goodbye. \r\n')


    # TODO: add active mode.
    '''
        only support passive mode now. 
    '''
    def PASV(self, cmd):
        # open data port
            self.passive_on = True
            self.socket_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_data.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
            self.socket_data.bind((HOST, 0))
            self.socket_data.listen(5)
            port = self.socket_data.getsockname( )[1]

            ip = HOST.split('.')
            ip = ','.join(ip)
            # port = port1 * 256 + port2
            port1 = port // 256
            port2 = port % 256
            # (ip,ip,ip,ip,port,port)
            ip_port = ip+','+str(port1)+','+str(port2)
            self.log('PASV','%s.'%ip_port)
            self.sendCmd('227 Entering Passive Mode (%s).\r\n'%ip_port)
            

        # def NOOP(self):

    
    '''
        send command to client
    '''
    def sendCmd(self, cmd):
        self.conn.send(cmd.encode('utf-8'))


    '''
        control data socket & send data to client
    '''
    def openDataSock(self):
        self.log('Open data sock', '...')
        # only passive mode 
        # socket_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dataConn, addr = self.socket_data.accept( )
        self.log('Open data sock', 'done.')
        # self.sendCmd('Data sock opened on %s.\r\n'%str(self.dataConn))

    def closeDataSock(self):
        self.log('Stop data sock', self.dataConn)
        self.dataConn.close()
        self.socket_data.close( )
        self.log('Stop data sock', 'closed.')
        # self.sendCmd('Data sock closed on %s.\r\n'%str(self.dataConn))

    def sendData(self, cmd):
        self.dataConn.send(cmd.encode('utf-8'))


    def log(self, fun, cmd):
        date_time = time.strftime("[ %Y-%m-%d %H:%M:%S ] " + fun)
        print(date_time, ">>", cmd)



    '''
        FTP funtions
    '''
    def PWD(self, cmd):
        self.log('PWD', cmd)
        self.sendCmd('257 %s.\r\n'%self.cwd)

    def CWD(self, path):
        self.log('CWD', path)
        if path == '':
            serverPath = LOCALDIR
        else:
            serverPath = os.path.join(self.cwd, path)
        serverPath = os.path.abspath(serverPath)
        print(serverPath)
        if serverPath and os.path.exists(serverPath):
            if os.path.commonprefix([LOCALDIR, serverPath]) == LOCALDIR:
                self.cwd = serverPath
                self.sendCmd("250 Directory changed to %s.\r\n"% path)
            else:
                self.sendCmd('550 Permission denied.\r\n')
        else:
            self.sendCmd('550 Directory not exists.\r\n')
            return


    def LIST(self, path):
        self.log('LIST',path)
        if not path:
            serverPath = self.cwd
        else:
            serverPath = os.path.join(self.cwd, path)

        # serverPath = os.path.join(LOCALDIR, curpath)
        print(serverPath)
        if not os.path.exists(serverPath):
            self.sendCmd('550 Path name not exists.\r\n')
            return
        self.sendCmd('150 Here is listing --- \r\n')
        self.openDataSock()
        if os.path.isdir(serverPath):       #   TODO: add detailed file information
            for file in os.listdir(serverPath):
                try:
                    self.sendData('- '+file+'\r\n') 
                except Exception as e:
                    self.log('LIST error', e)
        elif os.path.isfile(serverPath):
            name = os.path.basename(serverPath)
            try:
                self.sendData(name+'\r\n')
            except Exception as e:
                    self.log('LIST error', e)
        self.closeDataSock()
        self.sendCmd('226 List done.\r\n')
        # self.closeDataSock()
    
    def MKD(self, name):
        self.log('MKD', name)
        serverFname = os.path.join(LOCALDIR, name)
        try:
            os.mkdir(serverFname)
            self.sendCmd('257 Directory %s Created. \r\n'%name)
        except Exception as e:
            self.sendCmd('550 MKD failed : Directory "%s" already exists.\r\n' % serverFname)
    
    def TYPE(self, cmd):
        self.log('TYPE', cmd)
        if cmd == 'A':
            self.mode = 'A'
            self.sendCmd('200 Type set to A.\r\n')
        elif cmd =='I':
            self.mode = 'I'
            self.sendCmd('200 Type set to I.\r\n')


    def DELE(self, filename):
        filepath = os.path.join(self.cwd, filename)
        self.log('DELE', filepath)
        if not os.path.exists(filepath):
            self.sendCmd('550 File %s not exists.\r\n' % filepath)
        elif os.path.isfile(filename):
            os.remove(filepath)
        else:
            removeDir(filepath)
        self.sendCmd('250 File deleted. \r\n')
        

    def STOR(self, localpath):
        filename = os.path.basename(localpath)
        filepath = os.path.join(self.cwd, filename)
        try:    
            if self.mode == 'I':
                file = open(filepath, 'wb')
            else:
                file = open(filepath, 'w')
            self.log('STOR', filepath)
        except OSError as err:
            self.log('STOR', err)
        self.sendCmd('150 Start receiving file ... \r\n')
        self.openDataSock()
        while True:
            data = self.dataConn.recv(BUFSIZE)
            if not data:
                break
            file.write(data)
        file.close()
        self.closeDataSock()
        self.sendCmd('226 File transmission complete. \r\n')


    def RETR(self, filename):
        pathname = os.path.join(self.cwd, filename)
        self.log('RETR', pathname)
        if not os.path.exists(pathname):
            return
        try:
            if self.mode=='I':
                file = open(pathname, 'rb')
            else:
                file = open(pathname, 'r')
        except OSError as err:
            self.log('RETR', err)

        self.sendCmd('150 Opening data connection.\r\n')

        self.openDataSock( )
        while True:
            data = file.read(BUFSIZE)
            if not data: break
            self.sendData(data)
        file.close()
        self.closeDataSock( )
        self.sendCmd('226 Transfer complete.\r\n')

def connect():
        ip_port = (HOST, PORT)
        backlog = 5
        socket_cmd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_cmd.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) # 减少地址复用的时间
        socket_cmd.bind(ip_port)
        socket_cmd.listen(backlog)

        print('Server start:', 'listening on %s, port %s'% socket_cmd.getsockname( ))

        while True:
            conn, addr = socket_cmd.accept() # 等待连接
            ftp = MiniFTP(conn, addr)
            ftp.start()
            print('Connection Built', '%s, %s'%(conn,addr))

        socket_cmd.close()

if __name__ == "__main__":
    server = threading.Thread(target=connect)
    server.start()

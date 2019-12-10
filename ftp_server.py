# server
import os
import sys
import time
import socket
import subprocess
import threading

try:
    HOST = socket.gethostbyname(socket.gethostname( ))
except socket.gaierror:
    HOST = '127.0.0.1'
PORT = 21
BUFSIZE = 1024


class MiniFTP(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.serverAddr = addr
        self.welcomeMsg()


    def run(self):
        while True:
            try:
                data = self.conn.recv(BUFSIZE).rstrip()
                try:
                    cmd = data.decode('utf-8')
                except AttributeError:
                    cmd = data
                self.log('Received data', cmd)
                if not cmd:
                    break
            except socket.error as err:
                self.log('Receive', err)

            try:
                # cmd, arg = cmd[:4].strip(), cmd[4:].strip( ) or None
                command = cmd.split()[0]
                arg = cmd.split()[1:]
                arg = ' '.join(arg)
                func = getattr(self, command)
                func(arg)
            except AttributeError as err:
                self.sendCmd('500 Syntax error, command unrecognized. '
                    'This may include errors such as command line too long.\r\n')
                self.log('Receive', err)
  
    def USER(self, user):
        self.log("USER", user)
        if not user:
            self.sendCmd('501 Syntax error in parameters or arguments.\r\n')

        else:
            self.sendCmd('331 Enter password.\r\n')
            self.username = user

    def PASS(self, passwd): # TODO：修改明文传输密码
        self.log("PASS", passwd) 
        if not passwd:
            self.sendCmd('501 Syntax error in parameters or arguments.\r\n')

        elif not self.username:
            self.sendCmd('503 Bad sequence of commands.\r\n')

        else:
            self.sendCmd('230 User logged in, proceed.\r\n')
            self.passwd = passwd
            self.authenticated = self.loginAuth()
            if not self.authenticated:
                self.conn.close()

    def loginAuth(self):
        f = open('auth.config', 'r')
        for line in f.readlines():
            user, pswd = line.split()
            if user == self.username and pswd == self.passwd:
                self.log("Login", "success")
                self.conn.send("Success! log in as ", user)
                return True
        self.sendCmd('530 Login incorrect.')
        return False

    def QUIT(self):
        self.sendCmd('221 Goodbye. \r\n')
    def log(self, fun, cmd):
        date_time = time.strftime("[ %Y-%m-%d %H:%M:%S ] " + fun)
        print(date_time, ">>", cmd)


    def welcomeMsg(self):
        self.sendCmd('220 ---- Welcome to Portal of MiniFTP ---- \r\n')

    def sendCmd(self, cmd):
        self.conn.send(cmd.encode('utf-8'))
    

def connect():
        ip_port = (HOST, PORT)
        backlog = 5
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) # 减少地址复用的时间
        socket_server.bind(ip_port)
        socket_server.listen(backlog)

        print('Server start:', 'listening on %s, port %s'% socket_server.getsockname( ))

        while True:
            conn, addr = socket_server.accept() # 等待连接
            ftp = MiniFTP(conn, addr)
            ftp.start()
            print('Connection Built', '%s, %s'%(conn,addr))

        socket_server.close()
        # global listen_sock
        # listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 减少地址复用的时间
        # listen_sock.bind((HOST, PORT))
        # listen_sock.listen(5)

        # print('Server started', 'Listen on: %s, %s' % listen_sock.getsockname( ))
        # while True:
        #     connection, address = listen_sock.accept( )
        #     f = MiniFTP(connection, address)
        #     f.start( )
        #     print('Accept', 'Created a new connection %s, %s' % address)



if __name__ == "__main__":
    server = threading.Thread(target=connect)
    server.start()

    if input().lower() == "q":
        listen_sock.close( )
        print('Server closed')
        sys.exit( )
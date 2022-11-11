from socket import socket,AF_INET,SOCK_STREAM
import sys
from threading import Thread
from time import sleep

class transer(Thread):
    def __init__(self,identity,host=gethostname(),port=9993):
        super().__init__()
        
        self.serversocket = socket(AF_INET, SOCK_STREAM)
        
        if identity == "SERVEY": 
            self.serversocket.bind((host, port))
            self.serversocket.listen(2)
            print("连接地址：",host+":"+str(port))
            print("正在等待接入...")
            self.serversocket,addr = self.serversocket.accept()      
            print("连接成功...")
        
        elif identity == "CONNECTER":
            self.serversocket.connect((host, port))
            print("连接成功...")
        
        else:
            raise
            
        self.give = None
        self.back = None
        self.port = port
            
    def run(self):
        while True:
            if self.give:
                self.serversocket.send(self.give.encode('utf-8'))
                self.back = self.serversocket.recv(1024).decode("utf-8")
                self.give = None
            sleep(0.01)

if __name__ == "__main__":
    p = transer("CONNECTER")
    p.start()
    while 1: 
        p.give = "1234"
        print(p.back)
        sleep(1)
from asyncio.windows_events import NULL
import socket
import threading

from pprint import pprint as pp
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal

class SocketServer(QObject) :
    
    signal = pyqtSignal(dict) #클래스 변수로 선언

    #메시지 수신에 대한 처리 함수
    def RxThread(self, clientSocket, addr) :
        print('Connected by :', addr[0], ':', addr[1]) 

        while self.isConnect :
            try :
                data = clientSocket.recv(1024)

                if not data:
                    print('Disconnected by ' + addr[0],':',addr[1])
                    break

                print('Received from ' + addr[0],':',addr[1] , data.decode())
                self.rxCallbackFunc(data.decode())

            except ConnectionResetError as e:
                print('Disconnected by ' + addr[0],':',addr[1])
                break
        
        #pp(self.client_socket)
        self.SocketConnDisConnect(addr[0], addr[1])

        for key, val in self.client_socket.items() :
            if (val[2] == addr[0]) and (val[3] == addr[1]) :
                print( 'Del client socket [{} : ({}, {})]'.format(key, addr[0], addr[1]) )
                self.client_socket.pop(key)
                #self.updateClientInfoCallbackFunc(self.client_socket)
                self.signal.emit(self.client_socket) #customFunc 메서드 실행시 signal의 메서드 사용
                break        

    #Socket open에서 accept전 까지 처리
    def SocketOpen(self, host, port) :
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((host, port))
        self.serverSocket.listen()

        print("server start")

    #client 접속 대기 및 접속시 처리 부분
    def SocketConnect(self) :
        index = 0
        self.isConnect = True
        self.client_socket = {} # Client Socket informaion

        while self.isConnect:
            try:
                print("Wait for accept")
                clientSocket, addr = self.serverSocket.accept()
                clientInfo = (index, clientSocket, addr[0], addr[1]) #tuple for client information
                self.client_socket[index] = clientInfo
                pp(self.client_socket)
                print("{} is connected".format(addr))
                self.rcvThread = threading.Thread(target=self.RxThread, args=(clientSocket, addr)) 
                self.rcvThread.deamon = True           
                self.rcvThread.start()
                #self.updateClientInfoCallbackFunc(self.client_socket)
                self.signal.emit(self.client_socket) #customFunc 메서드 실행시 signal의 메서드 사용
                index += 1
            except OSError as err:
                print(err)


        print("Socket Close")
        self.serverSocket.close()

        if index > 0 : 
            self.rcvThread.join()

    #client socket이 disconnect되었을때 처리 부분
    def SocketConnDisConnect(self, addr, port) :
        print('[{} : {}] start disconnect'.format(addr, port))
        if self.isConnect is True :
            pp(self.client_socket)
            for key, val in self.client_socket.items() :
                if (val[2] == addr) and (val[3] == port) :
                    print('[{} : {}, {}] is disconnected'.format(val[0], val[2], val[3]))
                    val[1].close()

            print("Socket is disconnected")
        else :
            print("Socket is not connected")

    #server 소켓 close
    def SocketClose(self) :
        self.isConnect = False
        self.serverSocket.close()

    # 메시지 전송 부분
    def SocketSend(self, data) :
        if self.isConnect is True :
            print("send message : {}".format(data))
            pp(self.client_socket)
            for key, val in self.client_socket.items() :
                #print('type of val[1] is {}'.format(type(val[1])))
                val[1].send(bytes(data, 'utf-8'))

        else :
            print("Socket is not connected")

    #메시지 수신시 호출할 callback 함수 등록
    def RegRxCallbackFunc(self, func) :
        self.rxCallbackFunc = func

    #def RegClientInfoCallbackFunc(self, func) :
        #self.updateClientInfoCallbackFunc = func
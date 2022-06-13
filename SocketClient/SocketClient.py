import sys

import socket
import threading

class SocketClient() :
    #메시지 수신에 대한 처리 함수
    def RxThread(self) :
        while self.isConnect :
            try :
                data = self.clientSocket.recv(1024)

                if not data:
                    print('Disconnected ')
                    break

                print('Received : {} '.format(data.decode()))
                self.rxCallbackFunc(data.decode())

            except ConnectionResetError as e:
                print('Disconnected : '  + e)
                break

        self.clientSocket.close() 

    #Socket open에서 connect 까지 처리
    def SocketOpen(self, host, port) :
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.clientSocket.connect((host, port))
            print("Client start")
            self.isConnect = True
            self.rcvThread = threading.Thread(target=self.RxThread) 
            self.rcvThread.deamon = True           
            self.rcvThread.start()
        except OSError as err:
            print(err)

    #client 소켓 close
    def SocketClose(self) :
        self.isConnect = False
        self.clientSocket.close()

    # 메시지 전송 부분
    def SocketSend(self, data) :
        print("send message : {}".format(data))
        self.clientSocket.send(bytes(data, 'utf-8'))

    #메시지 수신시 호출할 callback 함수 등록
    def RegRxCallbackFunc(self, func) :
        self.rxCallbackFunc = func        


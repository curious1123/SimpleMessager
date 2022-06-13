import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

from SocketClient import SocketClient
import threading

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("client.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)    

        self.clientSocket = SocketClient() #Socket client 객체 생성

        self.sendBtn.clicked.connect(self.SendBtnEvent)                # send button에 대한 event 등록
        self.connectBtn.clicked.connect(self.ConnectBtnEvent)          # connect button에 대한 event 등록
        self.disconnectBtn.clicked.connect(self.DisconnectBtnEvent)    # disconnect button에 대한 event 등록
        self.menuexit.triggered.connect(self.AppExit)                  # 상단 menu bar의 exit에 대한 event 등록

        self.clientSocket.RegRxCallbackFunc(self.RxMessageProcess)     # 메시지 수신시 호출할 함수를 등록

    #상단 menu bar의 exit에 대한 구현 부
    def AppExit(self) :
        self.clientSocket.SocketClose()
        self.close()

    #Send 버튼에 대한 구현 부
    def SendBtnEvent(self) :
        print("send")
        #self.view.append(self.inputTxt.toPlainText())
        self.clientSocket.SocketSend(self.inputTxt.toPlainText())
        self.inputTxt.clear()
        
    #Connect 버튼에 대한 구현 부
    def ConnectBtnEvent(self) :
        print("connect")
        
        addr = self.inputServerAddr.toPlainText()
        port = int(self.inputPort.toPlainText())
        if (len(addr) > 0) and (port > 0) : 
            print("Try to connect to [addr : {}] [port : {}]".format(addr, port))
            self.clientSocket.SocketOpen(addr, port)
        else :
            print("Check server address and port")
    
    #disconnect 버튼에 대한 구현 부
    def DisconnectBtnEvent(self) :
        print("disconnect")
        self.clientSocket.SocketClose()

    #메시지 수신시 화면 출력
    def RxMessageProcess(self, data) :
        print('Rx Message : {}'.format(data))
        self.view.append(data)
        
if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()
    
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()        
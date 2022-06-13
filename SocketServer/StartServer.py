import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal

from SocketServer import SocketServer
import threading

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("server.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.serverSocket = SocketServer()                            # SocketServer 객체 생성

        self.sendBtn.clicked.connect(self.SendBtnEvent)               # send button에 대한 event 등록
        self.menuexit.triggered.connect(self.AppExit)                 # 상단 menu bar의 exit에 대한 event 등록
        self.connection.clicked.connect(self.ConnectBtnEvent)         # Start button에 대한 event등록
        self.disconnection.clicked.connect(self.DisConnectBtnEvent)   # Stop button에 대한 event등록
        self.serverSocket.RegRxCallbackFunc(self.RxMessageProcess)    # 메시지 수신시 호출할 함수를 등록
        self.serverSocket.signal.connect(self.UpdateClientInfomation) #객체에 대한 시그널 및 슬롯 설정.
        #self.serverSocket.RegClientInfoCallbackFunc(self.UpdateClientInfomation)
        print('initialized...')

    #Send 버튼에 대한 구현 부
    def SendBtnEvent(self) :
        self.view.append(self.inputText.toPlainText())
        self.serverSocket.SocketSend(self.inputText.toPlainText())
        self.inputText.clear()
    
    #상단 menu bar의 exit에 대한 구현 부
    def AppExit(self) :
        self.serverSocket.SocketClose()
        self.connThread.join()
        self.close()

    #Start 버튼에 대한 구현 부
    def ConnectBtnEvent(self) :
        print("socket connection")
        
        self.serverSocket.SocketOpen('127.0.0.1', 9999)
        self.connThread = threading.Thread(target=self.serverSocket.SocketConnect) 
        self.connThread.deamon = True           
        self.connThread.start()

    #Stop 버튼에 대한 구현 부
    def DisConnectBtnEvent(self) :
        print("socket disconnection start")
        self.serverSocket.SocketClose()
        self.connThread.join()
    
    #메시지 수신시 화면 출력
    def RxMessageProcess(self, data) :
        print('Rx Message : {}'.format(data))
        self.view.append(data)
        self.serverSocket.SocketSend(data)
    
    #접속한 Client정보 출력
    @pyqtSlot(dict)
    def UpdateClientInfomation(self, clientInfo) :
        self.clientInfoView.clear()
        for key, val in clientInfo.items() :
            self.clientInfoView.append("[{} : {}]".format(val[2], val[3]))



if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()
    
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
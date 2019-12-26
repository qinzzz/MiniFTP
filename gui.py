import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QRadioButton, QTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout, QMessageBox, QFileDialog, QComboBox
from PyQt5.QtCore import Qt,QObject,pyqtSignal
from PyQt5.QtGui import QTextCursor
import ftp_server

class EmittingStream(QObject):  
        textWritten = pyqtSignal(str)  #定义一个发送str的信号
        def write(self, text):
            self.textWritten.emit(str(text))

class Ftp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('''
			QLabel#h1{
			font-size:24px;
			font-weight:600;
			}
			''')
        self.title = "MiniFTP Server"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 540
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # linetext
        self.headLabel = QLabel("MiniFTP")
        self.headLabel.setObjectName('h1')
        self.portLabel = QLabel("Port:")
        self.portText = QLineEdit()
        self.portText.setText("21")
        self.dirLabel = QLabel("Local Directory:")
        self.dirText = QLineEdit()
        self.dirText.setText('/Users/qinzzz/ftp')
        self.confirmBtn = QPushButton("Open Server")
        self.closeBtn = QPushButton("Close")
        self.cancelBtn = QPushButton("Exit")

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        vboxTop = QVBoxLayout()
        hboxheadline = QHBoxLayout()
        hboxline1 = QHBoxLayout()
        hboxline2 = QHBoxLayout()

        hboxheadline.addWidget(self.headLabel,1,Qt.AlignCenter)
        hboxline1.addWidget(self.portLabel)
        hboxline1.addWidget(self.portText,1,Qt.AlignLeft)

        hboxline2.addWidget(self.dirLabel)
        hboxline2.addWidget(self.dirText,2,Qt.AlignLeft)
        hboxline2.addWidget(self.confirmBtn,Qt.AlignRight)
        hboxline2.addWidget(self.closeBtn,Qt.AlignRight)

        vboxTop.addLayout(hboxheadline)
        vboxTop.addLayout(hboxline1)
        vboxTop.addLayout(hboxline2)
        # vboxTop.addWidget(self.confirmBtn,Qt.AlignLeft)
        hboxBottom = QHBoxLayout()
        hboxBottom.addWidget(self.cancelBtn,Qt.AlignRight)
        # vboxMid = QVBoxLayout()
        # vboxMid = 

        vboxAll = QVBoxLayout()
        vboxAll.addLayout(vboxTop)
        vboxAll.addWidget(self.output)
        vboxAll.addLayout(hboxBottom)

        '''connection'''
        self.confirmBtn.clicked.connect(self.openServer)
        self.closeBtn.clicked.connect(ftp_server.closeSock)
        self.cancelBtn.clicked.connect(self.close)

        self.setLayout(vboxAll)
        self.show()

        sys.stdout = EmittingStream(textWritten=self.outputWritten)  
        sys.stderr = EmittingStream(textWritten=self.outputWritten)  
    
    #接收信号str的信号槽
    def outputWritten(self, text):  
        cursor = self.output.textCursor()  
        cursor.movePosition(QTextCursor.End)  
        cursor.insertText(text)  
        self.output.setTextCursor(cursor)  
        self.output.ensureCursorVisible()
	
    def openServer(self):
        if not self.portText.text():
            QMessageBox.information(self,'Fail','No port number entered.')
            return 
        port = int(self.portText.text())
        localdir = self.dirText.text()
        ftp_server.start(port, localdir)
		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = Ftp()
	sys.exit(app.exec_())



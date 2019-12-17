import sys
from BoardUI import BoardUI
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QDesktopWidget, QAction, qApp

class Tetris(QMainWindow):
    def __init__(self, title):
        super(Tetris, self).__init__()

        self.setWindowTitle(title)
        self.resize(BoardUI.pixWidth, BoardUI.pixHeight+30)
# 
        initWidget = QWidget(self)
        startButton = QPushButton('开始(S)')
        startButton.clicked.connect(self.gameStart)
        startButton.setShortcut('S')
       
        hbox = QHBoxLayout()  # 设置水平垂直居中
        hbox.addStretch(1)
        hbox.addWidget(startButton)
        hbox.addStretch(1)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        initWidget.setLayout(vbox)
        startButton.resize(100, 30)
        self.setCentralWidget(initWidget)
        
        self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, \
            (screen.height()-size.height())/2)

    def gameStart(self):
     
        self.UI = BoardUI(self)
        self.resize(BoardUI.pixWidth, BoardUI.pixHeight+30)

        self.sBar = self.statusBar()
        self.UI.msg2statusBar[str].connect(self.sBar.showMessage)

        self.setCentralWidget(self.UI)
        print(self.centralWidget())
        self.UI.start()


    def keyPressEvent(self, event):
        self.centralWidget().keyPressEvent(event) # 传递给centralWidget

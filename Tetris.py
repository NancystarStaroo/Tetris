from PyQt5.QtWidgets import QMainWindow, QWidget, QInputDialog, QPushButton, QHBoxLayout, QVBoxLayout, QDesktopWidget, QAction, qApp

import sys
from BoardUI import BoardUI

class Tetris(QMainWindow):
    def __init__(self, title):
        super(Tetris, self).__init__()

        self.setWindowTitle(title)
        self.resize(BoardUI.pixWidth, BoardUI.pixHeight+30)
# 
        initWidget = QWidget(self)
        startButton = QPushButton('开始')
        exitButton = QPushButton('退出')
        startButton.clicked.connect(self.gameStart)
        exitButton.clicked.connect(qApp.quit)
        startButton.setShortcut('S') #设置快捷方式

        hbox = QHBoxLayout()  # 设置水平垂直居中
        hbox.addStretch(1)
        hbox.addWidget(startButton)
        hbox.addWidget(exitButton)
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

        menubar = self.menuBar()
        gameActions = menubar.addMenu('&游戏')
        helpActions = menubar.addMenu('帮助')
        qexit = QAction('退出', self)
        qexit.setShortcut('Q')
        qpause = QAction('暂停', self)
        qpause.setShortcut('P')
        qrestart = QAction('重新开始', self)
        qrestart.setShortcut('R')
        qrank = QAction('查看排名', self)
        qrank.setShortcut('V')
        qhelp = QAction('反馈', self)
        qhelp.setShortcut('H')

        gameActions.addAction(qexit)
        gameActions.addAction(qpause)
        gameActions.addAction(qrestart)
        helpActions.addAction(qhelp)
        gameActions.addAction(qrank)

        qexit.triggered.connect(qApp.quit)
        qpause.triggered.connect(self.UI.PauseOrRestart)
        qrestart.triggered.connect(self.UI.restart)
        qhelp.triggered.connect(self.showDialog)
        qrank.triggered.connect(self.UI.viewRank)

        self.sBar = self.statusBar()
        self.UI.msg2statusBar[str].connect(self.sBar.showMessage)

        self.setCentralWidget(self.UI)
        print(self.centralWidget())

        self.UI.start()

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Feedback', 
            'Please input your feadback:')

        if ok:
            self.le.setText(str(text))

    def keyPressEvent(self, event): # 通过这种方法绕过Focus, 将keyEvent一直给centralWidget()
        self.centralWidget().keyPressEvent(event) # 传递给centralWidget


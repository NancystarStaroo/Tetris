from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QInputDialog, QPushButton, QHBoxLayout, QVBoxLayout, QDesktopWidget, \
    QAction, qApp, QLineEdit, QFrame, QMessageBox, QLabel, QGridLayout

from BoardUI import BoardUI

class Tetris(QMainWindow):
    def __init__(self, title):
        super(Tetris, self).__init__()

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon('icon.jpg'))
        self.resize(BoardUI.pixWidth, BoardUI.pixHeight+30)

        initWidget = QWidget(self)

        self.title = QLabel('账号:')
        self.password = QLabel('密码:')
        self.title_line = QLineEdit()
        self.password_line = QLineEdit()
        self.title_line.setPlaceholderText("请输入账号")
        self.password_line.setPlaceholderText("请输入密码")
        self.pushButton_enter = QPushButton()
        self.pushButton_quit = QPushButton()
        self.pushButton_enter.setText("登录")
        self.pushButton_enter.setShortcut('Enter')
        self.pushButton_quit.setText("取消")
        grid = QGridLayout()

        grid.setSpacing(5)
        grid.addWidget(self.title, 1, 0)
        grid.addWidget(self.title_line, 1, 1)
        grid.addWidget(self.password, 2, 0)
        grid.addWidget(self.password_line, 2, 1)
        grid.addWidget(self.pushButton_enter)
        grid.addWidget(self.pushButton_quit)

        self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit.clicked.connect(QCoreApplication.instance().quit)

        initWidget.setLayout(grid)
        self.setCentralWidget(initWidget)
        self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, \
            (screen.height()-size.height())/2)

    def gameStart(self):
        # pygame.init()
        # sound = pygame.mixer.Sound("C:\Users\Xuan\Music\纯音乐.wav")
        # sound.set_volume(1)
        # sound.play()
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
        qrank.triggered.connect(self.UI.showEmptyDialog)
     

        self.sBar = self.statusBar()
        self.UI.msg2statusBar[str].connect(self.sBar.showMessage)

        self.setCentralWidget(self.UI)
        print(self.centralWidget())

        self.UI.start()

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Feedback', 'Please input your feedback:')

        if ok:
            self.le.setText(str(text))

    def on_pushButton_enter_clicked(self):
        account = self.title_line.text()
        password = self.password_line.text()
        print(account, password)

        if account == 'admin' and password == '123456':
            self.gameStart()

        else:
            QMessageBox.warning(self, "警告", "用户名或密码错误！", QMessageBox.Yes)
            self.lineEdit.setFocus()

    def keyPressEvent(self, event):
        self.centralWidget().keyPressEvent(event)


from PyQt5.QtGui import QIcon, QColor, QBrush, QPainter
from PyQt5.QtWidgets import QApplication, qApp, QDialog, QWidget, QInputDialog, QMessageBox
from Shape import Shape
from PyQt5.QtCore import Qt, pyqtSignal, QBasicTimer


class BoardUI(QWidget):
    """游戏主要界面绘制，方块的绘制"""

    squareWidth = 30
    squareHeight = 30
    boardWidth = 10
    boardHeight = 20
    dropSpeed = 300
    pixWidth = squareWidth * boardWidth
    pixHeight = squareHeight * boardHeight
    msg2statusBar = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setWindowTitle("Game")
        self.resize(BoardUI.pixWidth, BoardUI.pixHeight)
        self.squares = []  # [x, y, color]
        self.X = 0
        self.Y = 0
        self.SQ = None
        self.removedLineNum = 0
        self.grade = []
        self.status = False  # True is start
        self.pause = False  # True is pause
        self.timer = QBasicTimer()

    def getPix(self, x, y):
        return [x*BoardUI.squareWidth, y*BoardUI.squareHeight]

    def RelPoints2AbsPoints(self, points):
        return [ [x+self.X, y+self.Y] for x, y in points ]

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        for x, y, color in self.squares:
            pixPoint = self.getPix(x, y)
            self.drawSquare(pixPoint, paint, event, color) # 绘制矩形

        try:
            for x, y in self.SQ.vertex:
                pixPoint = self.getPix(x+self.X, y+self.Y)
                self.drawSquare(pixPoint, paint, event, self.SQ.color)
        except AttributeError as e:
            print(e)
        
        paint.end()

    def drawSquare(self, point, paint, event, color):
        QCol = QColor()
        QCol.setNamedColor(color)
        paint.setBrush(QBrush(QCol))
        # paint.setPen(QCol)
        paint.drawRect(*point, BoardUI.squareWidth, BoardUI.squareHeight)

    def putShape(self):
        shape = Shape()
        shape.getRandomShape()
        self.SQ = shape
        self.X = BoardUI.boardWidth // 2  - 1 # 放到中间
        self.Y = abs(shape.yRange()[0])  # 最小的y值的绝对值

        if not self.canPut(self.SQ)[0]: # 一开始就放不了了 ， 那就是结束了
            self.timer.stop()
            self.status = False
            self.grade.append(str(self.removedLineNum))
            replay = QMessageBox.question(self, 'Message', 'Game Over! Do you want to play again?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if replay == QMessageBox.No:
                self.ignore()
            else:
                self.restart()

    def start(self):
        self.initBoard()
        self.status = True
        self.pause = False
        self.putShape()
        self.timer.start(BoardUI.dropSpeed, self)

    def initBoard(self): # 初始化面板
        self.squares.clear()
        self.X = 0
        self.Y = 0
        self.SQ = None
        self.removedLineNum = 0
        self.status = False
        self.pause = False
        self.msg2statusBar.emit('0')

    def timerEvent(self, event):
        self.Y = self.Y+1
        msg = self.canPut(self.SQ)
        if msg[1] == 'out of buttom' or msg[1] == 'overlap': # 到达底部或出现重叠就说明不能放了
            self.Y -= 1
            self.pushSquare(self.SQ)

        if not msg[0]:
            self.putShape()

        self.update()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_S:
            self.start()          
        elif self.status == False:
            pass
        elif key == Qt.Key_H:
            pass
        elif key == Qt.Key_V:
            pass
        elif key == Qt.Key_R:
            pass
        elif key == Qt.Key_O:
            self.sound.play
        elif key == Qt.Key_Q:
            qApp.quit()
        elif key == Qt.Key_P:
            self.PauseOrRestart()
        elif self.status == True and self.pause == True:
            pass
        elif key == Qt.Key_Left:  # 尝试向右移动，若可以就移动
            self.X -= 1
            if not self.canPut(self.SQ)[0]:
                self.X += 1
        elif key == Qt.Key_Right: # 尝试向右移动，若可以就移动
            self.X += 1
            if not self.canPut(self.SQ)[0]:
                self.X -= 1
        elif key == Qt.Key_Down:
            self.SQ.rotate('Clockwise')
            if not self.canPut(self.SQ)[0]:
                self.SQ.rotate('AntiClockwise')
        elif key == Qt.Key_Up:
            self.SQ.rotate('AntiClockwise')
            if not self.canPut(self.SQ)[0]:
                self.SQ.rotate('Clockwise')
        elif key == Qt.Key_Space:
            while self.canPut(self.SQ)[0]:
                self.Y += 1
            self.Y -= 1
        else:
            super().keyPressEvent(event) # 没有我们想要的就调用父类额

        self.update()

    def canPut(self, shape):  # 检查是否可以放
        points = shape.vertex
        minX = shape.xRange()[0] + self.X
        maxX = shape.xRange()[1] + self.X
        minY = shape.yRange()[0] + self.Y
        maxY = shape.yRange()[1] + self.Y

        if minX>=0 and maxX<BoardUI.boardWidth:
            pass
        else:
            return False, 'out of X'

        if minY>=0: 
            pass
        else:  
            return False, 'out of top'

        if maxY<BoardUI.boardHeight:
            pass
        else:
            return False, 'out of buttom'

        for *p,color in self.squares:
            if p in self.RelPoints2AbsPoints(shape.vertex):
                return False, 'overlap'

        return True, ''

    def readyRemoveLine(self):
        
        cnt = [0] * 20
        for x, y, c in self.squares:
            cnt[y] += 1
        
        self.removedLineNum += cnt.count(BoardUI.boardWidth) # 更新removedLineNum
        self.msg2statusBar.emit(str(self.removedLineNum))

        nSquare = []
        for x, y, c in self.squares:
            dy = 0
            for r in range(y, 20):
                if cnt[r] == BoardUI.boardWidth:
                    if y == r: # 该点要消除
                        break
                    else:  # r>y 该点要向下移一格
                        dy += 1

            else: # 无break就执行
                nSquare += [[x, y+dy, c]]

        self.squares = nSquare
        self.update()

    def PauseOrRestart(self):
        if not self.pause:
            self.pause = True
            self.timer.stop()
            self.msg2statusBar.emit('Pause')
        else:
            self.pause = False
            self.timer.start(BoardUI.dropSpeed, self)
            self.msg2statusBar.emit(str(self.removedLineNum))

    def pushSquare(self, shape):
        AbsPoints = self.RelPoints2AbsPoints(shape.vertex)
        
        self.squares += [[x, y, shape.color] for x, y in AbsPoints]

        self.readyRemoveLine()  # 检查是否删除

    def viewRank(self):
        pass

    def restart(self):
        self.initBoard()
        self.start()

    def showEmptyDialog(self):
        QMessageBox.information(self, "信息提示框", "你当前的分数是"+ str(self.removedLineNum) + "暂居第一名")


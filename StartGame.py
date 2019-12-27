import fix_qt_import_error
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication


from Tetris import Tetris

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Tetris('Tetris Game')
    game.show()
    sys.exit(app.exec_())
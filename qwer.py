import sys

import pygame as pygame
from PyQt5.QtWidgets import QApplication, QMainWindow


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        pygame.init()
        sound = pygame.mixer.Sound(r"此处为音频文件路径1.wav")
        sound.set_volume(1)
        sound.play()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.exit(app.exec_())
#!/usr/bin/env python3.5

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from Board import Board


class Game(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(200, 430)
        self.setWindowTitle('Tetris')
        self.tetBoard = Board(self)
        self.setCentralWidget(self.tetBoard)
        self.tetBoard.resize(200, 440)
        self.statusbar = self.statusBar()
        self.tetBoard.msg2statusbar[str].connect(self.statusbar.showMessage)
        self.tetBoard.start()
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = Game()
    sys.exit(app.exec_())

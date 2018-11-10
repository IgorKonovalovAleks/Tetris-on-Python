#!/usr/bin/env python3.5

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QLCDNumber
from PyQt5.QtCore import Qt
from Board import Board


class Game(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(400, 430)
        self.setWindowTitle('Tetris')
        self.scores = 0
        self.tetBoard = Board(self)
        self.lcd = QLCDNumber(self)
        self.tetBoard.resize(200, 415)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.tetBoard)
        self.layout.addWidget(self.lcd)
        self.lcd.move(250, 150)
        self.setLayout(self.layout)
        self.statusbar = self.statusBar()
        self.tetBoard.msg2statusbar[str].connect(self.statusbar.showMessage)
        self.tetBoard.closeMsg.connect(self.close)
        self.tetBoard.scoresMsg.connect(self.increase)
        self.tetBoard.start()
        self.show()

    def increase(self, score):
        self.scores += score
        self.lcd.display(self.scores)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = Game()
    sys.exit(app.exec_())

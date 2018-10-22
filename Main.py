import random
import random
import sys

from PyQt5.QtCore import QBasicTimer, Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame


class Game(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(200, 415)
        self.setWindowTitle('Tetris')
        self.tetBoard = Board(self)
        self.setCentralWidget(self.tetBoard)
        self.show()


class Board(QFrame):

    cube = 20
    figure = None

    def __init__(self, parent):
        super().__init__(parent)
        self.board = [0 for i in range(200)]
        self.timer = QBasicTimer()
        self.setFocusPolicy(Qt.StrongFocus)
        self.newTurn()

    def newTurn(self):
        self.dropFigure()
        self.figure = Figure()

    def dropFigure(self):
        for i in range(4):
            coord = self.figure.position[i][0] + self.figure.position[i][1] * 10
            for j in range(7):
                checkColor = DATA.getColor(j)
                if checkColor == self.figure.color:
                    self.board[coord] = j

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(200, 100, 100))
        for i in range(200):
            x = i % 10
            y = i - x * 10
            if self.board[i] != 0:
                tpl = DATA.getColor(self.board[i])
                qp.setBrush(QColor(tpl[0], tpl[1], tpl[2]))
                qp.drawRect(x * self.cube, y * self.cube, self.cube, self.cube)
        qp.setBrush(QColor(self.figure.color[0], self.figure.color[1], self.figure.color[2]))
        for i in range(4):
            qp.drawRect(self.figure.position[i][0] * self.cube, self.figure.position[i][1] * self.cube, self.cube, self.cube)
        qp.end()


class DATA(object):

    @staticmethod
    def getFigure(fig):
        return DATA._tetrominoe[fig]

    @staticmethod
    def getColor(fig):
        return DATA._colors[fig]

    _colors = ((198, 3, 3), (198, 123, 2), (109, 198, 1), (1, 198, 102), (1, 171, 198), (27, 1, 198), (168, 1, 198))
    _tetrominoe = (((0, 0), (0, 1), (1, 1), (1, 2)),
                   ((1, 0), (1, 1), (0, 1), (0, 2)),
                   ((0, 0), (1, 0), (1, 1), (1, 2)),
                   ((0, 0), (0, 1), (0, 2), (0, 3)),
                   ((0, 0), (0, 1), (0, 2), (1, 2)),
                   ((1, 0), (1, 1), (0, 2), (1, 2)),
                   ((0, 1), (1, 0), (1, 1), (2, 1)))


class Figure(object):

    shape = []
    position = []
    color = (0, 0, 0)

    def __init__(self):
        num = random.randint(0, 6)
        self._make(num)

    def _make(self, fig):
        sh = DATA.getFigure(fig)
        for i in range(4):
            peice = sh[i]
            self.shape.append([peice[0], peice[1]])
        self.color = DATA.getColor(fig)
        self.position = self.shape.copy()

    def move(self):
        pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = Game()
    sys.exit(app.exec_())
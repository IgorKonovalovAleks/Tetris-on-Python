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
        self.figure = Figure()
        self.timer.start(500, self)

    def newTurn(self):
        self.dropFigure()
        self.figure = Figure()

    def dropFigure(self):
        color = DATA.getColors().index(self.figure.color)
        for i in range(4):
            coord = self.figure.position[i][0] + self.figure.position[i][1] * 10
            self.board[coord] = color

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(200, 100, 100))
        for i in range(200):
            x = i % 10
            y = (i - x) / 10
            if self.board[i] != 0:
                tpl = DATA.getColor(self.board[i])
                qp.setBrush(QColor(tpl[0], tpl[1], tpl[2]))
                qp.drawRect(x * self.cube, y * self.cube, self.cube, self.cube)
        qp.setBrush(QColor(self.figure.color[0], self.figure.color[1], self.figure.color[2]))
        for i in range(4):
            qp.drawRect(self.figure.position[i][0] * self.cube,
                        self.figure.position[i][1] * self.cube, self.cube, self.cube)
        qp.end()

    def timerEvent(self, event):
        check = self.figure.nextPosition()
        for i in range(4):
            try:
                if self.board[check[1][i]] != 0:
                    break
            except IndexError:
                break
        else:
            if self.figure.move('down'):
                pass
            else:
                self.newTurn()
            self.update()
            return
        self.newTurn()
        self.update()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Left:
            self.figure.move('left')

        elif key == Qt.Key_Right:
            self.figure.move('right')

        self.update()


class DATA(object):

    @staticmethod
    def getFigure(fig):
        return DATA._tetrominoe[fig]

    @staticmethod
    def getColors():
        return DATA._colors

    @staticmethod
    def getColor(fig):
        return DATA._colors[fig]

    _colors = ((255, 255, 255), (198, 3, 3), (198, 123, 2), (109, 198, 1), (1, 198, 102), (1, 171, 198), (27, 1, 198), (168, 1, 198))
    _tetrominoe = ((),
                   ((0, 0), (0, 1), (1, 1), (1, 2)),
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
        self.shape = []
        self.position = []
        self.color = None
        num = random.randint(1, 8)
        self._make(num)

    def _make(self, fig):
        sh = DATA.getFigure(fig)
        for i in range(4):
            peice = sh[i]
            self.shape.append([peice[0], peice[1]])
        self.color = DATA.getColor(fig)
        self.position = self.shape.copy()

    def nextPosition(self):
        first = tuple()
        second = tuple()
        for i in range(4):
            first  += (self.position[i][1] + 1),
            second += (self.position[i][0] + self.position[i][1] * 10 + 10),
        return tuple((first, second))

    def move(self, mode):
        if mode == 'down':
            check = self.nextPosition()
            if 20 in check[0]:
                return False
            else:
                self._down()
                return True
        elif mode == 'left':
            self._left()
            return True
        elif mode == 'right':
            self._right()
            return True

    def _down(self):
        for i in range(4):
            self.position[i][1] += 1

    def _left(self):
        for i in range(4):
            if self.position[i][0] == 0:
                return
        for i in range(4):
            self.position[i][0] += -1

    def _right(self):
        for i in range(4):
            if self.position[i][0] == 9:
                return
        for i in range(4):
            self.position[i][0] += 1


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = Game()
    sys.exit(app.exec_())

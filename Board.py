from PyQt5.QtCore import QBasicTimer, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QFrame

from Data import DATA
from Figure import Figure


class Board(QFrame):

    cube = 20
    figure = None
    msg2statusbar = pyqtSignal(str)
    scores = 0

    def __init__(self, parent):
        super().__init__(parent)
        self.board = [0 for i in range(200)]
        self.timer = QBasicTimer()
        self.setFocusPolicy(Qt.StrongFocus)
        self.figure = Figure()

    def start(self):
        self.msg2statusbar.emit("Scores: " + str(self.scores))
        self.timer.start(500, self)

    def newTurn(self):
        newFigure = Figure()
        self.dropFigure()
        used = self._getUsedPlaces()
        for i in range(4):
            if tuple(newFigure.position[i]) in used:
                break
        else:
            self.figure = newFigure
            while self.removeFullLines():
                self.scores += 1
            self.msg2statusbar.emit("Scores: " + str(self.scores))
            return
        self.gameOver()

    def gameOver(self):
        self.timer.stop()
        self.msg2statusbar.emit("Game Over")

    def removeFullLines(self):
        for i in range(20):
            line = self.board[i * 10 : i * 10 + 10]
            for j in range(10):
                if line[j] == 0:
                    break
            else:
                j = i * 10 - 1
                while j != 10:
                    self.board[j + 10] = self.board[j]
                    j += -1
                return True
        return False

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
            y = (i - x) // 10
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
        used = self._getUsedPlaces()
        for i in range(4):
            if (check[i][0], check[i][1]) in used:
                break
        else:
            if self.figure.move('down', self._getUsedPlaces()):
                pass
            else:
                self.newTurn()
            self.update()
            return
        self.newTurn()
        self.update()

    def _getUsedPlaces(self):
        used = tuple()
        for i in range(200):
            if self.board[i]:
                x = i % 10
                used += (x, (i - x) // 10),
        return used

    def drop(self, used):
        while True:
            for i in range(4):
                nextPos = self.figure.nextPosition()
                if nextPos[i] in used or nextPos[i][1] == 20:
                    break
            else:
                self.figure.move('down', used)
                continue
            self.newTurn()
            break

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Left:
            self.figure.move('left', self._getUsedPlaces())

        elif key == Qt.Key_Right:
            self.figure.move('right', self._getUsedPlaces())

        elif key == Qt.Key_Up:
            self.figure.move('rotate right', self._getUsedPlaces())

        elif key == Qt.Key_Down:
            self.figure.move('rotate left', self._getUsedPlaces())

        elif key == Qt.Key_Space:
            self.drop(self._getUsedPlaces())

        self.update()
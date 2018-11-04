import random

from Data import DATA


class Figure(object):

    shape = []
    position = []
    color = (0, 0, 0)
    cube = False

    def __init__(self):
        self.shape = []
        self.position = []
        self.color = None
        num = random.randint(1, 7)
        if num == 5:
            self.cube = True
        else:
            self.cube = False
        self._make(num)

    def _make(self, fig):
        sh = DATA.getFigure(fig)
        for i in range(4):
            peice = sh[i]
            self.shape.append([peice[0], peice[1]])
            self.position.append([peice[0] + 1, peice[1] + 1])
        self.color = DATA.getColor(fig)

    def nextPosition(self):
        second = tuple()
        for i in range(4):
            second += (self.position[i][0], self.position[i][1] + 1),
        return second

    def move(self, mode, used):
        if mode == 'down':
            check = self.nextPosition()
            for i in range(4):
                if check[i][1] == 20:
                    return False
            self._down()
            return True
        elif mode == 'left':
            self._left(used)
            return True
        elif mode == 'right':
            self._right(used)
            return True
        elif mode == 'rotate right':
            self._rotateRight(used)
            return True
        elif mode == 'rotate left':
            self._rotateLeft(used)
            return True

    def _down(self):
        for i in range(4):
            self.position[i][1] += 1

    def _left(self, used):
        for i in range(4):
            if self.position[i][0] == 0 or (self.position[i][0] - 1, self.position[i][1]) in used:
                return
        for i in range(4):
            self.position[i][0] += -1

    def _right(self, used):
        for i in range(4):
            if self.position[i][0] == 9 or (self.position[i][0] + 1, self.position[i][1]) in used:
                return
        for i in range(4):
            self.position[i][0] += 1

    def _rotateRight(self, used):
        if self.cube:
            return
        newPosition = []
        newShape = []
        for i in range(4):
            newX = -self.shape[i][1] + self.position[i][0] - self.shape[i][0]
            newY = self.shape[i][0] + self.position[i][1] - self.shape[i][1]
            if 0 <= newX <= 9 and 0 <= newY <= 19 and tuple((newX, newY)) not in used:
                newPosition.append([newX, newY])
                newShape.append([-self.shape[i][1], self.shape[i][0]])
            else:
                return
        self.position = newPosition.copy()
        self.shape = newShape.copy()

    def _rotateLeft(self, used):
        if self.cube:
            return
        newPosition = []
        newShape = []
        for i in range(4):
            newX = self.shape[i][1] + self.position[i][0] - self.shape[i][0]
            newY = -self.shape[i][0] + self.position[i][1] - self.shape[i][1]
            if 0 <= newX <= 9 and 0 <= newY <= 19 and tuple((newX, newY)) not in used:
                newPosition.append([newX, newY])
                newShape.append([self.shape[i][1], -self.shape[i][0]])
            else:
                return
        self.position = newPosition.copy()
        self.shape = newShape.copy()
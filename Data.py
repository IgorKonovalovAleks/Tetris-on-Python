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
                   ((-1, -1), (0, -1), (0, 0), (0, 1)),
                   ((1, -1), (0, -1), (0, 0), (0, 1)),
                   ((-1, 0), (0, 0), (0, 1), (1, 1)),
                   ((-1, 1), (0, 1), (0, 0), (1, 0)),
                   ((0, 0), (0, 1), (1, 0), (1, 1)),
                   ((-1, 0), (0, 0), (1, 0), (2, 0)),
                   ((-1, 0), (0, 0), (1, 0), (0, 1)))
from enum import Enum

from models.City import City


class EuclidesPosition(Enum):
    Q1 = 1
    Q2 = 2
    Q3 = 3
    Q4 = 4
    AXIS_X_NEG = 5
    AXIS_X_POS = 6
    AXIS_Y_NEG = 7
    AXIS_Y_POS = 8
    CENTER = 9

    @classmethod
    def get_position(cls, x, y):
        if x == 0.0 and y > 0.0:
            return cls.AXIS_Y_POS
        elif x == 0.0 and y < 0.0:
            return cls.AXIS_Y_NEG
        elif x > 0.0 and y == 0.0:
            return cls.AXIS_X_POS
        elif x < 0.0 and y == 0.0:
            return cls.AXIS_X_NEG
        elif x > 0.0 and y > 0.0:
            return cls.Q1
        elif x < 0.0 < y:
            return cls.Q2
        elif x < 0.0 and y < 0.0:
            return cls.Q3
        elif x > 0.0 > y:
            return cls.Q4
        else:
            return cls.CENTER

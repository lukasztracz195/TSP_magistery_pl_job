import math


class City:


    @property
    def y(self):
        return self._y

    @property
    def x(self):
        return self._x

    def __init__(self, number_of_city, x, y):
        self._number_of_city = number_of_city
        self._x = x
        self._y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, City):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.x == other.x and self.y == other.y

    @staticmethod
    def count_distance(c1, c2):
        return math.sqrt(math.pow(c1.x - c2.x, 2) + math.pow(c1.y - c2.y, 2))

    @property
    def number_of_city(self):
        return self._number_of_city


    def __str__(self):
        return "City_number: %d | x: %d, y: %d" % (self.number_of_city, self.x, self.y)

    @y.setter
    def y(self, value):
        self._y = value

    @x.setter
    def x(self, value):
        self._x = value

    @number_of_city.setter
    def number_of_city(self, value):
        self._number_of_city = value

class Node:
    def __init__(self, parent, cost, index_city):
        if parent is None:
            self.__parent = None
            self.__cost = 0.0
            self.__way = []
            self.__way.append(index_city)
        else:
            self.__parent = parent
            self.__cost = parent.cost + self.cost
            self.__way.append(index_city)

        self.__index_city = index_city

    def __eq__(self, other):
        if not isinstance(other, Node):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.cost == other.cost

    def __le__(self, other):
        return self.cost < other.cost

    @property
    def index_city(self):
        return self.__index_city

    @property
    def parent(self):
        return self.__parent

    @property
    def way(self):
        return self.__way

    @property
    def cost(self):
        return self.__cost

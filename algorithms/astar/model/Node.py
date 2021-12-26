import copy


class Node:
    def __init__(self, parent, cost, index_city):
        self.__cost = cost
        self.__way = []
        self.__parent = parent
        if parent is not None:
            self.__cost = parent.cost + self.__cost
            self.__way = copy.deepcopy(parent.way)
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

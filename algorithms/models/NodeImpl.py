class Node:
    parent = None
    cost = 0
    way = list()
    index_of_city = 0
    can_be_visit = True

    def __init__(self, parent, cost, index_of_city):
        self.parent = parent

        if parent is not None:
            self.cost = parent.cost + cost
            self.way = list(parent.way)
        self.way.append(index_of_city)
        self.index_of_city = index_of_city

    def __lt__(self, other):
        return self.cost < other.cost

    def __le__(self, other):
        return self.cost <= other.cost

    def __eq__(self, other):
        return hash(self) == other.hash

    def __hash__(self):
        return hash((self.cost, self.way))

    def __ne__(self, other):
        return hash(self) != other.hash

    def __gt__(self, other):
        return self.cost > other.cost

    def __ge__(self, other):
        return self.cost >= other.cost

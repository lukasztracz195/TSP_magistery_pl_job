import copy


class Node:
    def __init__(self, parent, g_value, h_value, index_of_last_visited_city):
        self.__parent = parent
        self.__g_value = g_value  # red
        self.__h_value = h_value  # blue
        self.__gh_value = g_value + h_value  # green
        self.__way = []
        self.__available_next_nodes = list()
        self.__set_way_and_cost_basic_parent_node()
        self.__way.append(index_of_last_visited_city)
        self.__index_of_last_visited_city = index_of_last_visited_city

    def __hash__(self):
        return hash(str(self.way))

    def __ne__(self, other):
        return self.way != other.way

    def __lt__(self, other):
        return self.__gh_value < other.gh_value

    def __gt__(self, other):
        return self.__gh_value > other.gh_value

    def __le__(self, other):
        return self.__gh_value <= other.gh_value

    def __ge__(self, other):
        return self.__gh_value >= other.gh_value

    def __eq__(self, other):
        if not isinstance(other, Node):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.way == other.way

    @property
    def index_of_last_visited_city(self):
        return self.__index_of_last_visited_city

    @property
    def parent(self):
        return self.__parent

    @property
    def way(self):
        return self.__way

    @property
    def h_value(self):
        return self.__h_value

    @property
    def g_value(self):
        return self.__g_value

    @property
    def gh_value(self):
        return self.__gh_value

    @property
    def number_of_cities(self):
        return len(self.__way)

    @property
    def available_next_nodes(self):
        return self.__available_next_nodes

    def add_available_next_node(self, next_node):
        self.__available_next_nodes.append(next_node)

    def __set_way_and_cost_basic_parent_node(self):
        if self.__parent is not None:
            self.__way = copy.deepcopy(self.__parent.way)

import time
from typing import List

from scipy import rand

from algorithms.astar.model.Node import Node


class BrutalForce:
    def __int__(self, list_city, distance_matrix, start_city_number):
        self.__list_city = list_city
        self.__start_city_number = start_city_number
        self.__t0 = time.time()
        self.__t_stop = None
        self.__time_of_execution = None
        self.__distance_matrix = distance_matrix
        self.__nodes = list()
        self.__list_of_how_many_nodes_is_on_every_floor_of_tree = list()
        self.generate_list_of_how_many_nodes_is_on_every_floor_of_tree(len(list_city))

    @property
    def list_city(self):
        return self.__list_city

    @list_city.setter
    def list_city(self, value):
        self.__list_city = value

    @property
    def start_city_number(self):
        return self.__start_city_number

    @start_city_number.setter
    def start_city_number(self, value):
        self.__start_city_number = value

    @property
    def t0(self):
        return self.__t0

    @t0.setter
    def t0(self, value):
        self.__t0 = value

    @property
    def t_stop(self):
        return self.__t_stop

    @t_stop.setter
    def t_stop(self, value):
        self.__t_stop = value

    @property
    def time_of_execution(self):
        return self.__time_of_execution

    @time_of_execution.setter
    def time_of_execution(self, value):
        self.__time_of_execution = value

    @property
    def distance_matrix(self):
        return self.__distance_matrix

    @distance_matrix.setter
    def distance_matrix(self, value):
        self.__distance_matrix = value

    def generate_set_for_all_indexes_of_city(self):
        tmp_set = set()
        for index in range(0, len(self.list_city)):
            tmp_set.add(index)
        return tmp_set

    def generate_set_for_all_unvisited_indexes_of_city(self, parent):
        tmp_set = self.generate_set_for_all_indexes_of_city()
        for item in parent.way:
            tmp_set.remove(item)
        return tmp_set

    def generate_list_of_how_many_nodes_is_on_every_floor_of_tree(self, number_of_cities):
        self.__list_of_how_many_nodes_is_on_every_floor_of_tree.append(1)
        self.__list_of_how_many_nodes_is_on_every_floor_of_tree.append(number_of_cities - 1)
        multiplication_result = number_of_cities - 1
        substring = 2
        while (substring < number_of_cities):
            multiplication_result *= (number_of_cities - substring)
            self.__list_of_how_many_nodes_is_on_every_floor_of_tree.append(multiplication_result)

    def create_tree(self):
        for levelOfTree in range(0, len(self.__list_of_how_many_nodes_is_on_every_floor_of_tree)):
            for number_of_group in range(0, self.get_number_of_groups(levelOfTree)):
                if len(self.__nodes) == 0:
                    self.__nodes.append(Node(None, 0.0, self.__start_city_number))
                else:
                    temporary_set = set()
                    for nodes_in_one_group in range(0, self.get_number_of_nodes_in_group(number_of_group, levelOfTree)):
                        self.add_node_to_tree(temporary_set, number_of_group)

    def add_node_to_tree(self, temporary_set, number_of_group):
        self.deleted_visited_nodes(temporary_set, self.__nodes[number_of_group])
        selected_city = self.get_unique_index_of_city(temporary_set)
        if selected_city != -1:
            parent = None
            if len(self.__nodes) > 0:
                parent = self.__nodes[number_of_group]
            new_node = Node(parent, self.get_distance(parent.index_city, selected_city), selected_city)
            self.__nodes.append(new_node)

    def delete_unnecessary_nodes(self, list_nodes: List[Node], how_many):
        while len(list_nodes) > how_many:
            list_nodes.remove(0)

    def get_number_of_groups(self, level_fo_tree):
        return self.calculate_number_of_group(len(self.__list_of_how_many_nodes_is_on_every_floor_of_tree),
                                              self.get_number_of_groups(level_fo_tree))

    def get_number_of_nodes_in_group(self, level_of_tree):
        return self.__list_of_how_many_nodes_is_on_every_floor_of_tree[level_of_tree]

    def calculate_number_of_group(self, number_of_all_cities, level_of_tree):
        if level_of_tree < 2:
            return 1
        return (number_of_all_cities - (level_of_tree - 1)) * self.calculate_number_of_group(number_of_all_cities,
                                                                                             (level_of_tree - 1))

    def get_distance(self, city1, city2):
        return self.distance_matrix[city1, city2]

    def add_final_nodes(self):
        new_nodes = list()
        for item in self.__nodes:
            end_node = Node(item, self.get_distance(item.index_city, self.start_city_number), self.start_city_number)
            new_nodes.append(end_node)
        self.__nodes = new_nodes
        self.__nodes.sort()

    def get_unique_index_of_city(self, set_int):
        if len(set_int) != 0:
            size_of_set = len(set_int)
            selected = rand.randint(size_of_set)
            i = 0
            for item in set_int:
                if i == selected:
                    set_int.remove(item)
                    return item
                i += 1
        return -1

    def deleted_visited_nodes(self, set_int, parent):
        for item in parent.way:
            set_int.remove(item)

    def show_nodes(self):
        for node in self.__nodes:
            print(node)

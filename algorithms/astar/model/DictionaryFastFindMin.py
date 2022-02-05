import sys

from bisect import bisect_left

from algorithms.astar.model.treeset import TreeSet


class DictionaryFastFindMinMaxInNode:
    def __init__(self):
        self.__dictionary = dict()
        self.__min_value_of_key = sys.maxsize
        self.__max_value_of_key = -sys.maxsize
        self.__tree_set = TreeSet()

    def __getitem__(self, key):
        if key in self.__dictionary:
            return self.__dictionary[key]
        return None

    def key_exists(self, key):
        return key in self.__dictionary

    def add(self, key: float, value: min):
        if not self.key_exists(key):
            self.__dictionary[key] = value
            self.__tree_set.add(key)
            self.__update_min_value_of_key()
            self.__update_max_value_of_key()

    def pop(self, key, value):
        self.__dictionary.pop(key, value)
        self.__tree_set.remove(key)
        self.__update_min_value_of_key()
        self.__update_max_value_of_key()

    def get_sum_k_min(self, k):
        k_min_list = list()
        for i in range(0, k + 1):
            k_min_list.appendself.__tree_set[i]

    def clear(self):
        self.__dictionary.clear()
        self.__tree_set.clear()
        self.__min_value_of_key = sys.maxsize
        self.__max_value_of_key = -sys.maxsize

    def get_min_value_of_key(self):
        return self.__min_value_of_key

    def get_max_value_of_key(self):
        return self.__max_value_of_key

    def __update_min_value_of_key(self):
        self.__min_value_of_key = self.__tree_set[0]

    def __update_max_value_of_key(self):
        self.__max_value_of_key = self.__tree_set[len(self.__tree_set) - 1]

    # def __binary_search_in_order_list(self, value_to_search):
    #     size_of_list = len(self.__treeset)
    #     last_index = size_of_list - 1
    #     if size_of_list > 0:
    #         if self.__treeset[0] == value_to_search:
    #             return 0
    #         elif self.__treeset[last_index] == value_to_search:
    #             return last_index
    #         else:
    #             i = bisect_left(self.__treeset, value_to_search)
    #             if i != len(self.__treeset) and self.__treeset[i] == value_to_search:
    #                 return i
    #     return -1
    #
    # def __insert_key_to_good_position_in_list(self, key):
    #     size_of_list = len(self.__treeset)
    #     if size_of_list == 0:
    #         self.__treeset.append(key)
    #     elif key == self.__min_value_of_key and key == self.__max_value_of_key:
    #         self.__treeset.append(key)
    #     elif key < self.__min_value_of_key:
    #         self.__treeset.insert(0, key)
    #     elif key > self.__max_value_of_key:
    #         self.__treeset.append(key)
    #     else:
    #         number_of_elements = len(self.__treeset)
    #         center_index = int(number_of_elements / 2)
    #         left_index = 0
    #         right_index = number_of_elements - 1
    #         while True:
    #             center_value = self.__treeset[center_index]
    #             left_value = self.__treeset[left_index]
    #             right_value = self.__treeset[right_index]
    #             if left_index + 1 == right_index:
    #                 if left_value < key < right_value:
    #                     self.__treeset.insert(right_index, key)
    #                 else:
    #                     self.__treeset.insert(left_index, key)
    #                 break
    #             elif key < center_value:
    #                 right_index = center_index
    #                 center_index = int((left_index + right_index) / 2)
    #             elif key > center_value:
    #                 left_index = center_index
    #                 center_index = int((left_index + right_index) / 2)

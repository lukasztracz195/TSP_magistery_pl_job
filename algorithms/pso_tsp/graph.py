import random
import sys


class Graph:

    def __init__(self, amount_vertices):
        self.edges = {}  # dictionary of edges
        self.vertices = set()  # set of vertices
        self.amount_vertices = amount_vertices  # amount of vertices

    # adds a edge linking "src" in "dest" with a "cost"
    def addEdge(self, src, dest, cost=0):
        # checks if the edge already exists
        if not self.existsEdge(src, dest):
            self.edges[(src, dest)] = cost
            self.vertices.add(src)
            self.vertices.add(dest)

    # checks if exists a edge linking "src" in "dest"
    def existsEdge(self, src, dest):
        return (True if (src, dest) in self.edges else False)

    # shows all the links of the graph
    def showGraph(self):
        print('Showing the graph:\n')
        for edge in self.edges:
            print('%d linked in %d with cost %d' % (edge[0], edge[1], self.edges[edge]))

    # returns total cost of the path
    def getCostPath(self, path):

        total_cost = 0
        for i in range(self.amount_vertices - 1):
            total_cost += self.edges[(path[i], path[i + 1])]

        # add cost of the last edge
        total_cost += self.edges[(path[self.amount_vertices - 1], path[0])]
        return total_cost

    # gets random unique paths - returns a list of lists of paths
    def getRandomPaths(self, max_size):

        random_paths, list_vertices = [], list(self.vertices)

        initial_vertice = random.choice(list_vertices)
        if initial_vertice not in list_vertices:
            print('Error: initial vertice %d not exists!' % initial_vertice)
            sys.exit(1)

        list_vertices.remove(initial_vertice)
        list_vertices.insert(0, initial_vertice)

        for i in range(max_size):
            list_temp = list_vertices[1:]
            random.shuffle(list_temp)
            list_temp.insert(0, initial_vertice)

            if list_temp not in random_paths:
                random_paths.append(list_temp)

        return random_paths


# class that represents a complete graph
class CompleteGraph(Graph):

    # generates a complete graph
    def generates(self):
        for i in range(self.amount_vertices):
            for j in range(self.amount_vertices):
                if i != j:
                    weight = random.randint(1, 10)
                    self.addEdge(i, j, weight)

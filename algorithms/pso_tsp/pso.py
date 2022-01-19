import copy
import random
import sys
from operator import attrgetter

from algorithms.pso_tsp.particle import Particle


class PSO:

    def __init__(self, graph, iterations, size_population, beta=1, alfa=1):
        self.graph = graph  # the graph
        self.iterations = iterations  # max of iterations
        self.size_population = size_population  # size population
        self.particles = []  # list of particles
        self.beta = beta  # the probability that all swap operators in swap sequence (gbest - x(t-1))
        self.alfa = alfa  # the probability that all swap operators in swap sequence (pbest - x(t-1))

        # initialized with a group of random particles (solutions)
        solutions = self.graph.getRandomPaths(self.size_population)

        # checks if exists any solution
        if not solutions:
            print('Initial population empty! Try run the algorithm again...')
            sys.exit(1)

        # creates the particles and initialization of swap sequences in all the particles
        for solution in solutions:
            # creates a new particle
            particle = Particle(solution=solution, cost=graph.getCostPath(solution))
            # add the particle
            self.particles.append(particle)

        # updates "size_population"
        self.size_population = len(self.particles)

    # set gbest (best particle of the population)
    def setGBest(self, new_gbest):
        self.gbest = new_gbest

    # returns gbest (best particle of the population)
    def getGBest(self):
        return self.gbest

    # shows the info of the particles
    def showsParticles(self):

        print('Showing particles...\n')
        for particle in self.particles:
            print('pbest: %s\t|\tcost pbest: %d\t|\tcurrent solution: %s\t|\tcost current solution: %d' \
                  % (str(particle.getPBest()), particle.getCostPBest(), str(particle.getCurrentSolution()),
                     particle.getCostCurrentSolution()))
        print('')

    def run(self):

        # for each time step (iteration)
        for t in range(self.iterations):

            # updates gbest (best particle of the population)
            self.gbest = min(self.particles, key=attrgetter('cost_pbest_solution'))

            # for each particle in the swarm
            for particle in self.particles:

                particle.clearVelocity()  # cleans the speed of the particle
                temp_velocity = []
                solution_gbest = copy.copy(self.gbest.getPBest())  # gets solution of the gbest
                solution_pbest = particle.getPBest()[:]  # copy of the pbest solution
                solution_particle = particle.getCurrentSolution()[
                                    :]  # gets copy of the current solution of the particle

                # generates all swap operators to calculate (pbest - x(t-1))
                for i in range(self.graph.amount_vertices):
                    if solution_particle[i] != solution_pbest[i]:
                        # generates swap operator
                        swap_operator = (i, solution_pbest.index(solution_particle[i]), self.alfa)

                        # append swap operator in the list of velocity
                        temp_velocity.append(swap_operator)

                        # makes the swap
                        aux = solution_pbest[swap_operator[0]]
                        solution_pbest[swap_operator[0]] = solution_pbest[swap_operator[1]]
                        solution_pbest[swap_operator[1]] = aux

                # generates all swap operators to calculate (gbest - x(t-1))
                for i in range(self.graph.amount_vertices):
                    if solution_particle[i] != solution_gbest[i]:
                        # generates swap operator
                        swap_operator = (i, solution_gbest.index(solution_particle[i]), self.beta)

                        # append swap operator in the list of velocity
                        temp_velocity.append(swap_operator)

                        # makes the swap
                        aux = solution_gbest[swap_operator[0]]
                        solution_gbest[swap_operator[0]] = solution_gbest[swap_operator[1]]
                        solution_gbest[swap_operator[1]] = aux

                # updates velocity
                particle.setVelocity(temp_velocity)

                # generates new solution for particle
                for swap_operator in temp_velocity:
                    if random.random() <= swap_operator[2]:
                        # makes the swap
                        aux = solution_particle[swap_operator[0]]
                        solution_particle[swap_operator[0]] = solution_particle[swap_operator[1]]
                        solution_particle[swap_operator[1]] = aux

                # updates the current solution
                particle.setCurrentSolution(solution_particle)
                # gets cost of the current solution
                cost_current_solution = self.graph.getCostPath(solution_particle)
                # updates the cost of the current solution
                particle.setCostCurrentSolution(cost_current_solution)

                # checks if current solution is pbest solution
                if cost_current_solution < particle.getCostPBest():
                    particle.setPBest(solution_particle)
                    particle.setCostPBest(cost_current_solution)

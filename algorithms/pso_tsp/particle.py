class Particle:

    def __init__(self, solution, cost):
        # current solution
        self.solution = solution

        # best solution (fitness) it has achieved so far
        self.pbest = solution

        # set costs
        self.cost_current_solution = cost
        self.cost_pbest_solution = cost

        # velocity of a particle is a sequence of 4-tuple
        # (1, 2, 1, 'beta') means SO(1,2), prabability 1 and compares with "beta"
        self.velocity = []

    # set pbest
    def setPBest(self, new_pbest):
        self.pbest = new_pbest

    # returns the pbest
    def getPBest(self):
        return self.pbest

    # set the new velocity (sequence of swap operators)
    def setVelocity(self, new_velocity):
        self.velocity = new_velocity

    # returns the velocity (sequence of swap operators)
    def getVelocity(self):
        return self.velocity

    # set solution
    def setCurrentSolution(self, solution):
        self.solution = solution

    # gets solution
    def getCurrentSolution(self):
        return self.solution

    # set cost pbest solution
    def setCostPBest(self, cost):
        self.cost_pbest_solution = cost

    # gets cost pbest solution
    def getCostPBest(self):
        return self.cost_pbest_solution

    # set cost current solution
    def setCostCurrentSolution(self, cost):
        self.cost_current_solution = cost

    # gets cost current solution
    def getCostCurrentSolution(self):
        return self.cost_current_solution

    # removes all elements of the list velocity
    def clearVelocity(self):
        del self.velocity[:]

#
# genetic.py
#

import random
from math import pi
from simulation import Simulation
from walker import Walker

MAXIMIZE, MINIMIZE = 11, 22
#pos -- the initial position
# ul -- the length of the upper leg
# ll -- the length of the lower leg
# w -- the width of the robot
# lua -- the angle of the left hip
# lla -- the angle of the left ankle
# rua -- the angle of the right hip
# rla -- the angle of the right angle

class Individual(object):
    alleles = [[500,500], [350,350], [20,60], [5,60], [10,40], [pi/10, pi/60], [0,0],[0,0],[0,0]]
    length = 9
    seperator = ''
    optimization = MAXIMIZE

    def __init__(self, chromosome=None):
        self.chromosome = chromosome or self._makechromosome()
        self.score = None  # set during evaluation

    def _makechromosome(self):
        "makes a chromosome from randomly selected alleles."
        return [random.uniform(self.alleles[gene][0], self.alleles[gene][1]) for gene in range(self.length)]

    def evaluate(self,individual, optimum=None):
        self.score = 0
        s = Simulation(show=False)
        robot = Walker(s.space, [self.chromosome[0], self.chromosome[1]], self.chromosome[2], self.chromosome[3],\
        self.chromosome[4], self.chromosome[5], self.chromosome[6], self.chromosome[7], self.chromosome[8])
        energy = s.get_ke()
        currentPosition1 = s.step(0.02)
        energy = s.get_ke()
        count = 0
        while(energy > 2000 and count < 100):
            energy = s.get_ke()
            #print "Kinect Energy: "+str(energy)+" score =", self.score, " count: ", count
            currentPosition2 = s.step(0.02)
            #print "position: ",currentPosition1,  currentPosition2
            if currentPosition1 - currentPosition2 > 0.1:
                self.score+=1
                count = 0
            else:
                count +=1

            if self.score > 2000:
                self.simulate()
                break
            currentPosition1 = currentPosition2
        #print "Final Score: ", self.score

    def simulate(self):
        s = Simulation()
        robot = Walker(s.space, [self.chromosome[0], self.chromosome[1]], self.chromosome[2], self.chromosome[3],\
        self.chromosome[4], self.chromosome[5], self.chromosome[6], self.chromosome[7], self.chromosome[8])
        print "Simulating best Individual with score: ", self.score
        currentPosition = s.step(0.02)
        energy = s.get_ke()
        while(currentPosition > 0 and energy > 1):
            energy = s.get_ke()
            #print "currentPosition: ", currentPosition
            currentPosition = s.step(0.02)

    def crossover(self, other):
        "override this method to use your preferred crossover method."
        return self._twopoint(other)

    def mutate(self, gene):
        "override this method to use your preferred mutation method."
        self._pick(gene)

    # sample mutation method
    def _pick(self, gene):
        "chooses a random allele to replace this gene's allele."
        self.chromosome[gene] = random.uniform(self.alleles[gene][0], self.alleles[gene][1])

    # sample crossover method
    def _twopoint(self, other):
        "creates offspring via two-point crossover between mates."
        left, right = self._pickpivots()
        def mate(p0, p1):
            chromosome = p0.chromosome[:]
            chromosome[left:right] = p1.chromosome[left:right]
            child = p0.__class__(chromosome)
            child._repair(p0, p1)
            return child
        return mate(self, other), mate(other, self)

    # some crossover helpers ...
    def _repair(self, parent1, parent2):
        "override this method, if necessary, to fix duplicated genes."
        pass

    def _pickpivots(self):
        left = random.randrange(1, self.length-2)
        right = random.randrange(left, self.length-1)
        return left, right

    #
    # other methods
    #


    def __repr__(self):
        "returns string representation of self"
        chromosome_str = ''
        for gene in range (len(self.chromosome)):
            chromosome_str += ' ' + str(self.chromosome[gene])

        return '<%s chromosome="%s" \nscore=%s>' % \
               (self.__class__.__name__,
                chromosome_str, self.score)

    def __cmp__(self, other):
        if self.optimization == MINIMIZE:
            return cmp(self.score, other.score)
        else: # MAXIMIZE
            return cmp(other.score, self.score)

    def copy(self):
        twin = self.__class__(self.chromosome[:])
        twin.score = self.score
        return twin


class Environment(object):
    def __init__(self, kind, population=None, size=100, maxgenerations=400, \
                 generation=0, crossover_rate=0.8, mutation_rate=0.4, \
                 optimum=None):
        self.kind = kind
        self.size = size
        self.optimum = optimum
        self.population = population or self._makepopulation()
        for individual in self.population:
            individual.evaluate(individual, self.optimum)
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.maxgenerations = maxgenerations
        self.generation = generation
        self.report()

    def _makepopulation(self):
        return [self.kind() for individual in range(self.size)]

    def run(self):
        while not self._goal():
            self.step()
        #self.simulateBest()

    def _goal(self):
        return self.generation > self.maxgenerations or self.best.score == self.optimum

    def step(self):
        self.population.sort()
        self._crossover()
        self.generation += 1
        self.report()

    def _crossover(self):
        next_population = [self.best.copy()]
        while len(next_population) < self.size:
            mate1 = self._select()
            if random.random() < self.crossover_rate:
                mate2 = self._select()
                offspring = mate1.crossover(mate2)
            else:
                offspring = [mate1.copy()]
            for individual in offspring:
                self._mutate(individual)
                individual.evaluate(self.optimum)
                next_population.append(individual)
        self.population = next_population[:self.size]

    def _select(self):
        "override this to use your preferred selection method"
        return self._tournament()

    def _mutate(self, individual):
        for gene in range(individual.length):
            if random.random() < self.mutation_rate:
                individual.mutate(gene)

    #
    # sample selection method
    #
    def _tournament(self, size=8, choosebest=0.90):
        competitors = [random.choice(self.population) for i in range(size)]
        competitors.sort()
        if random.random() < choosebest:
            return competitors[0]
        else:
            return random.choice(competitors[1:])
    def returnBest(self):
        best = 0
        currentBest = None
        for individual in self.population:
            if individual.score > best :
                best = individual.score
                currentBest = individual
                #print "Score best so far: ", currentBest.score
        return currentBest

    def simulateBest(self):
        self.bestIndividual = self.returnBest()
        print "Best at the end:", self.bestIndividual
        self.bestIndividual.simulate()

    def best():
        doc = "individual with best fitness score in population."
        def fget(self):
            return self.population[0]
        return locals()
    best = property(**best())

    def report(self):
        print "="*70
        print "generation: ", self.generation
        print "best:       ", self.best

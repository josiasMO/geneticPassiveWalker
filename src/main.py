from genetic import Individual, Environment
from walker import Walker
from simulation import Simulation

env = Environment(Individual)
env.run()
while True:
    env.simulateBest()

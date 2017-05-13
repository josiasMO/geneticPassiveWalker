from genetic import Individual, Environment
from walker import Walker
from simulation import Simulation

env = Environment(Individual)
env.run()
while True:
    env.simulateBest()
# s = Simulation()
# pos = [500,350]
# robot = Walker(s.space, pos, 71.432066135, 34.7654718482, 15.2583435925, 0.075796370585, 0, 0, 0)
# energy = s.get_ke()
# s.step(0.02)
# energy = s.get_ke()
# iteracao = 0
# while(energy >  1):
#     energy = s.get_ke()
#     print "Kinect Energy "+str(iteracao)+": "+str(energy)
#     s.step(0.02)
#     iteracao+=1

# space -- the pymunk space
# pos -- the initial position
# ul -- the length of the upper leg
# ll -- the length of the lower leg
# w -- the width of the robot
# lua -- the angle of the left hip
# lla -- the angle of the left ankle
# rua -- the angle of the right hip
# rla -- the angle of the right angle

#500.0, 350.0] 71.432066135 34.7654718482 15.2583435925 0.075796370585 0.0 0.0 0.0


# print "chromosome: "+str(individual.chromosome)
#

#
#
#

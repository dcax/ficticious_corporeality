from .core import * #Giving Error: Attempted Relative Import in Non-Package
from .constants import *
from .subsystems import *
from .plotting import *

import scipy.constants as const


def test_suite():
    plot(verse_trial_1())

#test
def verse_trial_1():
    square = ParallelogramBoundary(
        np.array([10,10,0]),
        np.array([0,10,0]),
        np.array([0,0,0]),
        uniform_margin=.1)

    sheet1 = Sheet(name="major1", boundary=square, uniform_mass=1, n=5, m=5, constrained_movement=True, vertical_tension=10, horiz_tension=10)
    sheet1.clump[1,1].v = np.array([0.0,0.0,10.0])

    v = Verse1()

    manager = VerseManager(initial_conditions=Instant.make_instant_from_subsystems([sheet1]),verse=v)

    manager.progress(n= 10000, sample= lambda i, n: {i.report(n=n)}, every=1000,ignoring_first=0)
    return manager






#tests

def verse_trial_2(): #This test is designed to see how the parallelogram deals with chirality
    square = ParallelogramBoundary(
        np.array([10,10,0]),
        np.array([10,0,0]),
        np.array([0,0,0]),
        uniform_margin=.1)

    sheet1 = Sheet(name="major2", boundary=square, uniform_mass=1, n=5, m=5, constrained_movement=True, vertical_tension=10, horiz_tension=10)
    sheet1.clump[1,1].v = np.array([0.0,0.0,10.0])

    v = Verse1()

    manager = VerseManager(initial_conditions=Instant.make_instant_from_subsystems([sheet1]),verse=v)

    manager.progress(n= 10, sample= lambda i, n: {i.report(n=n)}, every=3,ignoring_first=0)




def brownian_motion_trial0(relative_strength=1.0):
    #This tests simple 10 particle brownian motion
    print("Trial with relative strength {}.".format(relative_strength))


    particles = 10 #number particles
    blob = BoundlessBoundary() #creates standard spatial boundary
    trials = 2000000 #number trials
    every = 50000 #frequency of documentation
    particle_store = np.empty((1,trials//every,particles,2)) #contains description of particle to be used in data population
    #test 0: for stationary field
    field = np.ones(3)*1.0E3*relative_strength
    stuff = OhmicMaterial.init_by_randomly_populating(boundary=blob, electric_field=field,num=10)
    stuff.damping = 1.0E-10
    stuff.sigma = 1.0E-3 #np.sqrt(2*stuff.damping*const.k*298)
    v = Verse1() #verse object controls moving forward

    #creates a manager to do aux functions on the verse
    manager = VerseManager(initial_conditions=Instant.make_instant_from_subsystems([stuff]), verse=v)
    manager.progress(n=trials,every=every, ignoring_first=0, store_every=every)

    records = []
    for p in manager.now.notable:
        #iterates over notable particles and puts their record in public location
        records.append(p.history)

    #print([r["r"] for r in records])
    #print([r["v"] for r in records])
    #for record in records:
        #print(record)

    print() #"Got here!")
    print() #adds some whitespace for asethetics

    #exit()
    #computes the summary statistics
    average_positions = [np.array([record['rx'].mean(),record['ry'].mean(),record['rz'].mean()]) for record in records]
    average_momentums = [np.array([record['vx'].mean(),record['vy'].mean(),record['vz'].mean()]) for record in records]
    #print("Got past calculating both means.")
    #pprint(average_positions)
    std_dev_positions = [np.array([record['rx'].std(),record['ry'].std(),record['rz'].std()]) for record in records]
    #print("Got past calculating std dev for pos.")
    std_dev_momentums = [np.array([record['vx'].std(),record['vy'].std(),record['vz'].std()]) for record in records]

    #print("Testing")

    for i in range(len(records)):
        print("Particle {} has initial position ({},{},{}) and average position {} with sigma = {}.".
            format(i,records[i].iloc[0]['rx'],records[i].iloc[0]['ry'],records[i].iloc[0]['rz'],
            average_positions[i],std_dev_positions[i]))
        print("\tand average momentum {} with sigma = {}.".format(average_momentums[i],std_dev_momentums[i]))
        print("")

def do_brownian_experiment():
    brownian_motion_trial0(1)
    brownian_motion_trial0(2)
    brownian_motion_trial0(4)
    brownian_motion_trial0(8)
    brownian_motion_trial0(16)
    brownian_motion_trial0(32)





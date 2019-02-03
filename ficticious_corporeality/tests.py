from .core import *
from .constants import *
from .subsystems import *
from .plotting import *

def test_suite(gui=True):
    manager = verse_trial_1()
    if gui:
        plot(manager)
    verse_trial_2()

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

    manager.progress(n= 10, sample= lambda i, n: {i.report(n=n)}, every=2,ignoring_first=0)
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

from .core import *
from .constants import *
from .subsystems import *

def test_suite():
    verse_trial_1()


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

    manager.progress(n= 1000, sample= lambda i, n: {i.report(n=n)}, every=2,ignoring_first=0)

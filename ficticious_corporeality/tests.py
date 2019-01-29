from core import *
from constants import *
from subsystems import *

def test_suite():
    verse_trial_1()



def verse_trial_1():
    square = ParallelogramBoundary(
        np.array([10,10,0]),
        np.array([10,0,0]),
        np.array([0,0,0]),
        uniform_margin=.1)
    
    sheet1 = Sheet(boundary=square, uniform_mass=1, n=5, m=5, constrained_movement=True, vertical_tension=5, horiz_tension=5)

    v = Verse1()

    manager = VerseManager(initial_conditions=Instant.make_instant_from_subsystems([sheet1]),verse=v)

    manager.progress(n= 100, sample= lambda i, n: {i.report(n=n)}, every=20,ignoring_first=25)


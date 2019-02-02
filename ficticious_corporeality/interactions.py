import numpy as np
import pandas as pd

class Interaction:
    #interaction between 2 particles (essentially a tagged tuple)
    def __init__(self, x=None, y=None, newtonian=True, **kwargs):
        assert x is not None
        assert y is not None
        self.x = x
        self.y = y
        self.newtonian = newtonian


    def enact(self):
        #performs interaction on two particles.
        #Assumes newtonian and that interaction only works between two particles and not many.

        if not self.newtonian:
            assert False #This cannot happen

        #print("Enacting interaction on pair of particles.")
        #forces
        f = self.x.findForce(origin=self.y)
        self.x.apply(force=f)
        self.y.apply(force=-f) #Uses Newton's third Law

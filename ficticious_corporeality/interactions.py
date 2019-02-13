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

class SubsystemInteraction: 
    def __init__(self, subsystem=None, p=None, newtonian=True, **kwargs):
        assert p is not None
        assert subsystem is not None
        self.subsys = subsystem
        self.p = p
        self.newtonian = newtonian


    def enact(self):
        #performs interaction on two particles.
        #Assumes newtonian and that interaction only works between two particles and not many.

        if not self.newtonian:
            assert False #This cannot happen

        #print("Enacting interaction on pair of particles.")
        #forces
        f = self.subsys.find_subsystem_force(on=self.p)
        self.p.apply(force=f)
        #force does usually affect subsys, but will add this
        #self.y.apply(force=-f) #Uses Newton's third Law
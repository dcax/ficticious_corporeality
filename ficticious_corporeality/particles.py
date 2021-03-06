from .constants import *
from .utility import get_unit_vector, apply

import numpy as np
import pandas as pd

class Particle:
    #By default exists in 3D space.

    #X: loc[0], Y:loc[1], Z:loc[2]
    #Has mass and charqe inately
    #also can store itself selectively (as time series)

    def do_impulse(self, dp = np.zeros(3)):
        #does some impulse to a particle
        self.dv += dp/self.m #unused

    def __init__(self, mass=1.0, charge=0.0, loc=np.array([0.0,0.0,0.0]), velocity=np.array([0.0,0.0,0.0]), **kwargs):

        self.m = mass
        self.loc = loc
        self.v = velocity
        self.q = charge

        self.dm = 0.0
        self.dv = np.array([0.0,0.0,0.0])
        self.history = np.zeros(0)#pd.DataFrame(data=None,index=np.arange(0))  #usually this should be series
    



    def p(self):
        #returns momentum
        return self.m * self.v

    def abs_p(self): #absolute value/magnitude of momentum
        return np.linalg.norm(self.p())

    def update(self):
        #update values after a stage.
        #print("Non contained update!")

        self.m += self.dm #I dont expect to need to change mass, but IDK.

        #simple Euler's method.
        self.loc += (self.v+self.dv/2)*dt
        self.v += self.dv

        #resetting values of importance
        self.dm = 0
        self.dv = np.array([0.0,0.0,0.0])

    def find_force(self,origin=None):

        assert origin is not None
        #This finds the force from the particles but does not apply anything.
        return 0

    def apply(self,force=0.0):
       apply(force=force,to=self)

    def __str__(self):
        return "Particle @ ({},{},{}) with p = {} and velocity = {}.".format(self.loc[0],self.loc[1],self.loc[2],self.abs_p(),self.v)



class ContainedParticle(Particle):
    #container deals with forces and with movement

    def __init__(self, mass=1, loc=np.array([0.0, 0.0, 0.0]), velocity=np.array([0.0, 0.0, 0.0]), container=None, container_loc=None, **kwargs):
        super().__init__(mass=mass, loc=loc, velocity=velocity, **kwargs)
        assert container is not None
        self.container = container
        self.container_loc = container_loc #used for better printing
        self.loc = loc


    def find_force(self, origin=None):
        assert origin is not None
        #print("Finding force.")
        return self.container.find_force(to=self, origin=origin)

    def apply(self, force=0):

        #Movement happens in container.
        self.container.apply(force=force,to=self)

    def update(self):
        #prefers modernizing through container.
        self.container.update(self)

    def __str__(self):
        return self.container.stringify(self)


##UNUSED
class LinkedParticle(Particle): #Particle linked to neighbors which do not themselves need to be Linked.

    def __init__(self, mass=1, loc=np.array([0.0, 0.0, 0.0]), velocity=np.array([0.0, 0.0, 0.0]), **kwargs):
        super().__init__(mass=mass, loc=loc, velocity=velocity, **kwargs)

        assert self.v == velocity

        self.links = []

    def link(self,to=[]):
        #Links particle to neighbors.
        if isinstance(to,Particle):
            self.links.append(to)
        else:
            self.links.extend(to)


class BoundaryParticle(Particle):
    pass
    #particle with boundary mechanism built in.


def dist(x,y): #gets euclidean distance between points
    if isinstance(x,Particle) and isinstance(y,Particle):
        #distance defined by positions
        x = x.loc
        y = y.loc
    return np.linalg.norm(x,y)

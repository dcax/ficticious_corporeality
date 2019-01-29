from Constants import *
from utility import *

import numpy as np
import pandas as pd

class Particle:
    #By default exists in 3D space.
    

    def __init__(self, mass=1, loc=np.array([0.0,0.0,0.0]), velocity=np.array([0.0,0.0,0.0]), **kwargs):
        
        self.m = mass
        self.loc = loc
        self.v = velocity

        self.dm = 0
        self.dv = np.array([0.0,0.0,0.0])

    def p(self):
        #returns momentum
        return self.m * self.v
    
    def abs_p(self): #absolute value/magnitude of momentum
        return np.linalg.norm(self.p)
    
    def update(self):
        #update values after a stage.

        self.m += self.dm #I dont expect to need to change mass, but IDK.

        #simple Euler's method.
        self.loc += (self.v+self.dv/2)*dt
        self.v += self.dv

        #resetting values of importance
        self.dm = 0
        self.dv = np.array([0.0,0.0,0.0])
    
    def findForce(self,origin=None):

        assert origin is not None
        #This finds the force from the particles but does not apply anything.
        return 0
    
    def apply(self,force=0):
       apply(force=force,to=self)
    
    def __str__(self):
        return "Particle @ ({},{},{}) with p = {}".format(self.loc[0],self.loc[1],self.loc[2],self.abs_p())


class ContainedParticle(Particle):
    #container deals with forces and with movement

    def __init__(self, mass=1, loc=np.array([0.0, 0.0, 0.0]), velocity=np.array([0.0, 0.0, 0.0]), container=None, container_loc=None, **kwargs):
        super().__init__(mass=mass, loc=loc, velocity=velocity, **kwargs)
        assert container is not None
        self.container = container
        self.container_loc = container_loc

    def findForce(self, origin=None):
        assert origin is not None
        self.container.findForce(to=self, origin=origin)
    
    def apply(self, force=0):

        #Movement happens in container.
        self.container.apply(force=force,to=self)
    
    def update(self):
        #prefers modernizing through container.
        self.container.modernize(self)
    
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



        

        



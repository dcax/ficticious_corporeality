import scipy as sc
import numpy as np
from .path_geometry import *
from .utility import *

#This contains all of the more advanced geometric primitives for multi surfaces.

#triangle is primitive because it only has rotational about a collective axis and not a single bond
class Triangle(ClosedPath):
    def __init__(self, x0, x1, x2):
        super().__init__(array=[x0,x1,x2])
        # suppose difference
        #self.n = self
    #only three points

    def normal(self):
        x0, x1, x2 = self.points
        if isinstance(x0,Particle): #assume all particles
            h = x1.loc - x0.loc #horizontal axis
            v = x2.loc - x0.loc #vertical axis
        h = x1 - x0 #horizontal axis
        v = x2 - x0 #vertical axis

        return get_unit_vector(np.cross(h,v))


class Tri(Traingle): #type synonym for triangle
    pass

class PointTriangle(Triangle): #triangle subject to physical laws
    #idealised as 3 points subject to rotational and translational motion

    #used mainly in deformable bodies
    def __init__(self, p0, p1, p2, omega):
        super().__init__(p0, p1, p2)
        #masses for optimised movement since this only needs to be calculated once
        self.masses = np.asarray([p.mass for p in self.points])

        
    def apply(self,force=np.zeros(3),location=np.zeros(3)):
        #force is applied rotationally and with torque at some point
        #point is assumed to be in triangle.
        p0, p1, p2 = self.points

        """loc = location
        r0 = p0.loc - loc #vector from point of application to vertex
        r1 = p1.loc - loc
        r2 = p2.loc - loc
        m0, m1, m2 = self.masses

        #would save as constant if particles did not move about center of mass
        I = m0*r0*r0 + m1*r1*r1 + m2*r2*r2

        cm = (m0*r0 + m1*r1 + m2*r2)/(m0 + m1 + m2)
        
        """
        p0.apply(force=force)
        p1.apply(force=force)
        p2.apply(force=force)


        #moment of inertia about location of interaction of force
    









from .utility import *

import numpy as np
import pandas as pd


#### This contains the code for regions in space.
### More complicated bounds constructed from simpler ones. 

class Boundary:
    def __str__(self):
        return ""

    pass #most general boundary

class RegularBoundary(Boundary):
    pass #some unspecified properties

class RandomBoundary(Boundary):
    #interface for a boundary that randomly picks points in it.

    def __init__(self, *args, **kwargs):
        pass

    def random_point(self):
        return np.zeros(3) #purposes is randomly selecting a point to create a particle

class BoundlessBoundary(RandomBoundary):
    #dumb boundary for testing purposes and unifying the framework.
    #pretty much all of space
    def __init__(self,center=np.zeros(3), sigma = 1.0):
        self.center = center #points will normally be distributed around center
        self.sigma = sigma #standard deviation of random point

    def random_point(self):
        point = np.random.normal(size=3,loc=self.center,scale=self.sigma)
        #print("Point randomly chosen: {}.".format(point))
        return point

class ParallelogramBoundary(RegularBoundary):
    #Boundary with parallogram outer segment.
    #Uniquely specified by three points.
    #Points specified in refrence frame of origin (universal) 
    # and specified counterclockwise starting in quadrant II.

    #TODO: FIX ordering because this is too sensistive to handedness.

    def __init__(self, x0=np.zeros(3), x1=np.zeros(3), x2=np.zeros(3), uniform_margin=0):
        super().__init__()
        self.uniform_margin = uniform_margin # margin within this boundary construct. 
        self.points = [x0, x1, x2, x0 + x2 - x1]
        h, v = self.axes()
        self.normal = np.cross(h,v) #Normal vector for constrained movement.
        #makes unitary assuming has length (non degenerate parallelogram)
        self.normal = get_unit_vector(self.normal)

    def length(self):
        #somewhat arbitrary on what side is length and what is width.
        #calculated on fly more expensive but this should run about once per instance.
        return np.linalg.norm(self.points[0]-self.points[1])
    
    def height(self):
        return np.linalg.norm(self.points[0]-self.points[2])

    def axes(self):
        #return horizontal,vertical axes in frame of boundary
        return (self.points[1]-self.points[0],self.points[2]-self.points[0])

    def locus(self):
        #returns focus point of parallelogram
        return self.points[0]

    def __str__(self): #This represents a parallelogram as a string for printing
        return "Parallelogram with points {}, {}, {}, {}.".format(self.points[0], self.points[1], self.points[2], self.points[3])
    
    


    
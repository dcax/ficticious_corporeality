from Particles import *
from Boundary import *
from Interactions import *
from Constants import *
from utility import *


### This contains the bulk of the subsystems defined for Verse1. 
import numpy as np
import pandas as pd

class Subsystem: 
    #contains properties of subsystems and boundaries. Individually contians particles.

    def __init__(self, boundary=None, name="Cal"):
        self.boundary = boundary
        self.name = name
        self.clump = []
        pass
    
    def interactions(self):
        pass



class Sheet(Subsystem): #Linear subsystem (runs in O(number objects = n*m))
    #contains rubbersheet schematics
    #Assume particles evenly spaced and linked at four points.
    #Particles constrained to move along normals only (optional). 
    #Params:
    #- Horizontal tension, vertical tension.
    #- n by m
    #- particless mass (uniform)
    #- distance between 

    def __init__(self, name="Cal", n=1,m=1, uniform_mass=1, boundary=None, constrained_movement=True, vertical_tension=0, horiz_tension=0):

        assert boundary is not None
        assert isinstance(boundary, ParallelogramBoundary) 
        # so far only parallelogram boundary supported

        super().__init__(boundary=boundary, name=name)

        self.constrained = constrained_movement
        self.vertical_tension = vertical_tension
        self.horiz_tension = horiz_tension

        self.locus = boundary.locus()
        self.n = n #Number particles in horiz dir
        self.m = m #Number particles in vertical dir
        self.mass = uniform_mass

        self.horiz_axis, self.vertical_axis = self.boundary.axes()
        self.normal = self.boundary.normal

        self.margin = self.boundary.uniform_margin
        self.length = self.boundary.length() - 2*self.boundary.uniform_margin
        self.height = self.boundary.height() - 2*self.boundary.uniform_margin

        self.horiz_scale = self.length / self.m
        self.vertical_scale = self.height / self.n

        assert self.length > 0
        assert self.height > 0

        self.init_clump()
       
        ##Link particles for ease.


    def report_subsystem(self): #reports the data as strings
        print("Subsystem: {}.".format(self.name))
        for index, particle in np.ndenumerate(self.clump):
            print("\t"+particle)



    def init_clump(self):
         ##Init particles
        self.clump = np.zeros(self.m * self.n).reshape((self.m,self.n))
        self.past_interactions = []

        dh =  get_unit_vector(self.horiz_axis) * self.horiz_scale
        dv = get_unit_vector(self.vertical_axis) * self.vertical_scale

        #start is initial refrence frame adjusted for bounds.
        start = self.locus + self.horiz_axis * self.margin + self.vertical_axis * self.margin

        for i in range(self.m):
            for j in range(self.n):
                loc = start + i*dh + j*dv

                

                p = ContainedParticle(container=self,mass=self.mass,loc=loc, container_loc=(i,j)) #Inits linked particle at location with Euler.
                self.clump[i,j] = p

                ##Adding interactions
                if j >= 1:
                    interaction = Interaction(p,self.clump[i,j-1],newtonian=True)
                    self.past_interactions.append(interaction)
                if i >= 1:
                    interaction = Interaction(p,self.clump[i-1,j],newtonian=True)
                    self.past_interactions.append(interaction)


    
    def interactions(self):
        #does not include boundaries
        #assume particle only interacts with neighbors (4 particles)
        #Assume newtonian context so that one interaction suffices for many.
        number_interactions = 2*(self.n-1)*(self.m-1) #DOES NOT INCLUDE BOUNDARY CONDITIONS
        #Draw out graph to find this. 

        #interactions = np.ones(shape=number_interactions, dtype=tuple, order='C')
        ### Here we initialise an object to be populated and returned later.

        #interactions = pd.DataFrame()

         
        ###Assume fixed interactions

        interactions = self.past_interactions

        assert len(interactions) == number_interactions

        return interactions

    def findForce(self, to = None, origin = None):
        #This works for linear displacement tension as is used on modeling sheets
        displacement = origin.loc - to.loc
        normal_displacement = project_onto_unit_vector(displacement,unit=self.normal)
        force = np.zeros(3)
        if(to.container_loc[0] == origin.container_loc[0]):
            #Same i, same horizontal position therefore displacement from vertical
            force += (self.vertical_tension/self.vertical_scale) * normal_displacement
        elif(to.container_loc[1] == origin.container_loc[1]):
            #Same j, same vertical position therefore displacement from horizontal
            force += (self.horiz_tension/self.horiz_scale) * normal_displacement
        
        return force



    def apply(self,force=0, to=None):
        apply(force=force,to=self)


    def update(self, p=None):
        assert p is not None
        p.m += p.dm #I dont expect to need to change mass, but IDK.

        #simple Euler's method.
        dr = (p.v+p.dv/2)*dt
        if self.constrained: 
            p.loc += project_onto_unit_vector(dr,unit=self.normal)
        else:
            p.loc += dr

        p.v += p.dv
        p.dm = 0
        p.dv = np.array([0.0,0.0,0.0])

    def stringify(self,p):
        #renders a particle a string
        return "Particle in subsys {} @ ({},{},{}) with p = {}".format(self.name, p.loc[0],p.loc[1],p.loc[2],p.abs_p())


#TODO: Boundaries, strings attatched, stiff strings, etcetera. 
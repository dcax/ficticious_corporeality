from .particles import *
from .boundary import *
from .interactions import *
from .constants import *
from .utility import *


### This contains the bulk of the subsystems defined for Verse1.
import numpy as np
import pandas as pd

class Subsystem:
    #contains properties of subsystems and boundaries. Individually contians particles.

    def __init__(self, boundary = None, name="Cal", plot_config=None):
        self.boundary = boundary # boundary not neccessary for defining a subsystem, but here for efficiency
        self.name = name
        self.plot_config = plot_config #Plot config control the way that plots are configured
        self.clump = np.array([])
        pass

    def get_particles(self):
        return np.asarray(self.clump.flatten())

    def interactions(self):
        pass

    def report_subsystem(self): #reports the data as strings
        print("Subsystem: {}.".format(self.name))

        print("With boundary {}.".format(self.boundary))

        for index, particle in np.ndenumerate(self.clump):
            print("\t"+str(particle))





class Sheet(Subsystem): #Linear subsystem (runs in O(number objects = n*m))
    #contains rubbersheet schematics
    #Assume particles evenly spaced and linked at four points.
    #Particles constrained to move along normals only (optional).
    #Params:
    #- Horizontal tension, vertical tension.
    #- n by m
    #- particless mass (uniform)
    #- distance between

    def __init__(self, plot_config=None, name="Cal", n=1,m=1, uniform_mass=1, boundary=None, constrained_movement=True, vertical_tension=0, horiz_tension=0):

        assert boundary is not None
        assert isinstance(boundary, ParallelogramBoundary)
        # so far only parallelogram boundary supported

        super().__init__(boundary=boundary, plot_config=plot_config, name=name)

        self.boundary = boundary

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
        assert type(self.margin) is float
        self.length = self.boundary.length() - (2*self.boundary.uniform_margin)
        self.height = self.boundary.height() - (2*self.boundary.uniform_margin)

        self.horiz_scale = self.length / self.m
        self.vertical_scale = self.height / self.n

        assert self.length > 0
        assert self.height > 0

        self.init_clump()

        ##Link particles for ease.





    def init_clump(self):
         ##Init particles
        self.clump = np.empty(shape=(self.m,self.n), dtype=object)
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
        #From wrong model: number_interactions = 2*(self.n-1)*(self.m-1) #DOES NOT INCLUDE BOUNDARY CONDITIONS
        #Draw out graph to find this.

        #interactions = np.ones(shape=number_interactions, dtype=tuple, order='C')
        ### Here we initialise an object to be populated and returned later.

        #interactions = pd.DataFrame()


        ###Assume fixed interactions

        interactions = self.past_interactions
        #print("interactions found, expected = {}, {}.".format(len(interactions), number_interactions))
        #assert len(interactions) == number_interactions

        return interactions

    def findForce(self, to = None, origin = None):
        #This works for linear displacement tension as is used on modeling sheets
        displacement =  origin.loc - to.loc
        normal_displacement = project_onto_unit_vector(displacement,unit=self.normal)
        force = np.zeros(3)
        if(to.container_loc[0] == origin.container_loc[0]):
            #Same i, same horizontal position therefore displacement from vertical
            force += (self.vertical_tension/self.vertical_scale) * normal_displacement
        elif(to.container_loc[1] == origin.container_loc[1]):
            #Same j, same vertical position therefore displacement from horizontal
            force += (self.horiz_tension/self.horiz_scale) * normal_displacement

        #print("Finding force on object {} from {}.".format(to,origin))
        #assert np.linalg.norm(force) == 0.0

        return force



    def apply(self,force=0.0, to=None):
        apply(force=force,to=to)


    def update(self, p=None):
        assert p is not None
        p.m += p.dm #I dont expect to need to change mass, but IDK.

        #if(np.linalg.norm(p.dv) != 0.0):
        #   print("Updating particle {} with dv = {}.".format(p,p.dv))

        #simple Euler's method.
        dr = (p.v + p.dv/2)*dt
        if self.constrained:
            p.loc += project_onto_unit_vector(dr,unit=self.normal)
        else:
            p.loc += dr

        p.v += p.dv
        p.dm = 0.0
        p.dv = p.dv * 0.0

    def stringify(self,p):
        #renders a particle a string
        return "Particle in subsys {} @ ({},{},{}) with p = {} at velocity = {}.".format(self.name, p.loc[0],p.loc[1],p.loc[2],p.abs_p(),p.v)


#TODO: Boundaries, strings attatched, stiff strings, etcetera.

class String(Subsystem):
    #String is a subsystem consisting of linked particles along a path.

    @staticmethod
    def make_string(uniform_mass=1, mass = None, count=1, path=None):
        #mass is a function that determines the mass of each particle
        assert path is not None and isinstance(path, )



    def __init__(self, plot_config=None, boundary=None, name='Ariadne', particles=[]):
        super().__init__(name=name, plot_config=plot_config, boundary=boundary)
        self.clump = np.array(particles)




class SpringSheet(Sheet):
    pass #This will represent a sheet capable of transverse and logitudonal (general) oscillations
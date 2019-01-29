
from .boundary import *
from .subsystems import *

import scipy, matplotlib

import numpy as np
import pandas as pd
from pprint import pprint



class VerseManager: 
    #This codifies the way the universe progresses from instant to instant.
    #Provides general functions to use in actually calculating values.
    def __init__(self, initial_conditions, verse, *args, **kwargs):
        assert initial_conditions is not None
        #IC Should be recieved and considered as type instant.
        assert isinstance(initial_conditions,Instant)
        assert isinstance(verse,Verse)


        self.now = initial_conditions
        self.verse = verse



    def perturb(self): 
        # do 1 intreval.
        self.verse.perturb(self.now)
        
        #self.now = self.verse.perturb(old)
    
    def progress(self, n, sample=lambda instant, n: {}, every=0, ignoring_first=0):
        ## moves universe forward n steps
        ##option to run sampling function every some such times ignoring the first some values.
        for i in range(n):
            self.perturb()
            if(i >= ignoring_first and every is not 0 and i % every == 0):
                sample(self.now, i)

        










class Instant:
    #This is a universe object and contians the nature of the project.
    #particles stored in clump. 

    @staticmethod
    def make_instant_from_subsystems(subsystems=[]):
        clump = []
        for subsys in subsystems:
            clump.extend(np.asarray(subsys.clump.flatten()))
        instant = Instant(clump=clump,subsystems=subsystems,misc=[],newtonian=True)
        return instant

    def __init__(self, clump=[], subsystems=[], misc=[], newtonian=True, **kwargs):
        #this creates a universe from nothing. 
        self.clump = clump
        self.subsystems = subsystems
        self.misc = misc #particles not in subsys.
        #subsystems are parts of the system with boundary conditions.
        pass
    
    def report(self, n = None):
        if n is not None:
            print("n = {}.".format(n))
        for subsystem in self.subsystems:
            subsystem.report_subsystem()
            print("")



        
    

class Verse:
    #This is the general pattern for universes of particles and evolving them
    #Represents a stationary universe. 
    def __init__(self, newtonain=True, *args, **kwargs):
        self.newtonian = newtonain
    
    def interactions(self,instant):
        #Takes pairs of particles and gets interactions pairs efficiently.
        #Does not include forcing
        return []
    
    def force(self,instant,time):
        #does forcing terms. Boundaries?
        #Instant time dependent.
        pass

    def perturb(self,old):
        #Takes old instant and produces new instant.
        pass
        #Too general without third law and superposition.

class Verse1(Verse):
    #This is a standard universe object that has our specifications about how it should work.

    #Newtonian, fixed interactions, forcing option, conserved particle number. 
    #Also forces superimpose, leading to easier computation. 

    def __init__(self, **kwargs):
        super().__init__( newtonian=True, **kwargs)

        self.interactions_register = [] #initialise interactions
    
    def interactions(self,instant):
        #only computes this once at beginning.
        if len(self.interactions_register) != 0:
            return self.interactions_register
        

        #this uses newton's third and fixed particle number and subsystems to find efficient interactions.
        #clump = instant.clump
        subsystems = instant.subsystems
        for subsys in subsystems:
            assert isinstance(subsys, Subsystem)
            #pprint(subsys.interactions())
            self.interactions_register.extend(subsys.interactions())
        
        #Do something with mischelaneos particles.
        return self.interactions_register



    def perturb(self, old):
        #super().perturb(old)
        interactions = self.interactions(old)
        #pprint(interactions)
        for interaction in interactions:
            interaction.enact()

        #forcing terms

        #modernize.
        #pprint(vars(old))
        for particle in old.clump:
            particle.update()
        #modernize kills old data and loads new









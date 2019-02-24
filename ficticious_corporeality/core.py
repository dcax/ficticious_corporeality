
from .boundary import *
from .subsystems import *

import scipy, matplotlib

import numpy as np
import pandas as pd
from pprint import pprint

from colorama import init as colorama_init


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

        #initialize the colorama library for printing colored text in the terminal
        colorama_init()


    def perturb(self):
        # do 1 intreval.
        self.verse.perturb(self.now)

        #self.now = self.verse.perturb(old)
    
    def progress(self, n, sample=lambda instant, n: {}, every=0, ignoring_first=0, store_every=None):
        ## moves universe forward n steps
        ##option to run sampling function every some such times ignoring the first some values.

        #particle_record_schema = np.dtype([('m',np.float64),('q',np.float64, 3),('r',np.float64),('v',np.float64, 3)]) 
        #this is basically a strucutred record that is optimised
        
        if store_every is not None: #This stores the value in an array that each particle keeps.
            entry_count = n//store_every
            
            for p in self.now.notable:
                p.history = pd.DataFrame(columns=["m","q","vx","vy","vz","rx","ry","rz"], index=np.arange(n//store_every), dtype=np.float64)
                #np.zeros(dtype=particle_record_schema, shape=entry_count)
                #pd.DataFrame(dtype=particle_record_schema, )
                #pd.DataFrame(columns=["m","q","v","r"], index=np.arange(n//store_every))
                #here we initialise history for each object of the requisite length

        for i in range(n):

            if(store_every is not None and i % store_every == 0):
                #here we cause the particle to store its data
                for p in self.now.notable:
                    #record = {"m": p.m, "q": p.q, "v": p.v, "r": p.loc}
                    
                    #print("Storing {} for {}-th time.".format(p,i//store_every))

                    record = p.history.iloc[i//store_every]
                    record['m'] = p.m
                    record['q'] = p.q
                    record['rx'] = p.loc[0]
                    record['ry'] = p.loc[1] #stores them component wise
                    record['rz'] = p.loc[2]
                    record['vx'] = p.v[0]
                    record['vy'] = p.v[1]
                    record['vz'] = p.v[2]
                    #reg = p.history.iloc[i//store_every]
                    

                    #loc copies record to row.
                    #this saves particle data
                

            if(i >= ignoring_first and every is not 0 and i % every == 0):
                sample(self.now, i)
            #we do sampling first so as to consider better changes (but last time is superfluous)

            self.perturb()
            

            

     










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
        self.notable = clump #ideally clump and notable are different, because we only want to document some particles, not all
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
        self.system_interactions_register = []
    
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
    
    def system_interactions(self, instant):
        #gets interactions with system (damping, forcing, walls, etcetera)
        if len(self.system_interactions_register) != 0:
            return self.system_interactions_register
        
        for subsys in instant.subsystems:
            assert isinstance(subsys,Subsystem)
            self.system_interactions_register.extend(subsys.subsystem_interactions())
        
        return self.system_interactions_register



    def perturb(self, old):
        #super().perturb(old)
        interactions = self.interactions(old)
        system_interactions = self.system_interactions(old)
        #pprint(interactions)
        for interaction in interactions:
            interaction.enact()

        #forcing terms
        for system_interaction in system_interactions:
            system_interaction.enact()

        #modernize.
        #pprint(vars(old))
        for particle in old.clump:
            particle.update()
        #modernize kills old data and loads new

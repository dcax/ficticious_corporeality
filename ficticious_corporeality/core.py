
import scipy, numpy, matplotlib

dt = .0001 #in s. Time intreval used. 


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


        return super().__init__(*args, **kwargs)

    def perturb(self): 
        # do 1 intreval.
        old = self.now

        self.now = self.verse.perturb(old)
    
    def progress(self, n, sample=lambda instant: {}, every=0, ignoring_first=0):
        ## moves universe forward n steps
        ##option to run sampling function every some such times ignoring the first some values.
        for i in range(n):
            self.perturb()
            if(i >= ignoring_first and every is not 0 and i % every == 0):
                sample(self.now)

        










class Instant:
    #This is a universe object and contians the nature of the project.
    #particles stored in clump. 

    def __init__(self, clump=[], newtonian=True, **kwargs):
        #this creates a universe from nothing. 
        pass
    


class Verse():
    #This is the general pattern for universes of particles and evolving them
    #Represents a stationary universe. 
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)
    
    def interactions(self,instant):
        #Takes pairs of particles and gets interactions pairs efficiently.
        #Does not include forcing
        return []
    
    def forcing(self,instant,time):
        #does forcing terms. Boundaries?
        pass

    def perturb(self,old):
        #Takes old instant and produces new instant.
        interactions = self.interactions(old)



class Verse1(Verse):
    #This is a standard universe object that has our specifications about how it should work.

    #Newtonian, fixed interactions, forcing option, fixed particles. 

    def __init__(self, clump=[], **kwargs):
        super().__init__(clump=clump, newtonian=True, **kwargs)

        self.interactions = None #initialise interactions
    
    def interactions(self,instant):
        if self.interactions is not None:
            return
        pass
        #this uses newton's third and fixed particles to find efficient interactions.







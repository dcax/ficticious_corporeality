
import numpy as np
from .constants import *

#This includes the utilitiy functions for stuffy like applying forces and torques at a point to nonrigid bodies.

####DO NOT USE THIS

def find_apply(force=np.zeros(3),location=np.zeros(3), particles = None, masses= None):
        #radii to point of pushing (where force is about)
        assert particles is not None
        loc = location
        particles = np.asarray(particles)
        if masses is None:
            masses = np.apply_along_axis(lambda p: p.mass,0,particles)
        radii = np.apply_along_axis(lambda p: p.loc - loc, 0 , particles) #this finds vectors that lead to particle from point of application

        #now we find moment of intertia
        #first we get r_squared array using elemnt wise multiplication
        r_squared = np.multiply(radii,radii)

        I = np.dot(r_squared,masses) #This is the quantity defined as moments of inertia
        #elsewhere moments of inertia is defined differently, 
        # must it is belt to calculate it dynamically for non rigid bodies.
        
        #now we can apply newton's second law of rotational motion.
        center = cm(particles= particles, masses = masses)
        R = loc - center #position of center with respect to loc
        torque = R.cross(force)

        alpha = torque/I #by rotational second law
        #alpha it second derivative of angle. It is rotational accelerations

        np.apply_along_axis(lambda p: p.apply(force=force),0,particles)



def cm(particles= None, masses = None): #This finds the center of mass in the origin frame.
    assert particles is not None
    
    particles = np.asarray(particles)
    if masses is None:
        masses = np.apply_along_axis(lambda p: p.mass,0,particles)
    locs = np.apply_along_axis(lambda p: p.loc, 0, particles) #finds the positions of all particles in the origin frame

    total_mass = np.sum(masses) #this should not be zero
    assert total_mass >= 0

    #takes linear combination by mass and normalises
    return np.transpose(locs).dot(masses) / total_mass

    







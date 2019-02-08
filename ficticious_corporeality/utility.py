from .constants import *

from pprint import pprint
import numpy as np

from colorama import Back, Style

# Gets unit or direction vector associated with the vector (v).
def get_unit_vector(v):
    l = np.linalg.norm(v)
    assert l is not 0.0
    return v/l

def apply(force=0.,to=None):
    #applies force to particle (does not actually move it (that happens in modernize))
    assert to is not None
    #Euler's method:
    #pprint(force)
    to.dv += force*dt/to.m #Uses superposition of impulses

def project_onto_unit_vector(v=None,unit=None):
    assert v is not None and unit is not None
    #we assume used properly so that there is not a necessary check on this each time.
    return np.dot(v,unit)*unit

def project_ortho_to_unit_vector(v=None,unit=None):
    return v - project_onto_unit_vector(v,unit)

#returns a string representing an array with postive numbers being green and negative numbers red
def colorize_vector(vector=None):
    #TODO: assert vector is [numpy array]

    output = "["
    for i in range(vector.size):
        #give negative numbers a red background and positive numbers a green background
        if vector[i] < 0:
            output += Back.RED
        elif vector[i] > 0:
            output += Back.GREEN
        
        output += str(vector[i]) + Style.RESET_ALL

        if i < vector.size - 1:
            output += " "

    output += "]"
    return output
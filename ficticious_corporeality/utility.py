from Constants import *

import numpy as np

def get_unit_vector(v):
    l = np.linalg.norm(v)
    assert l is not 0
    return v/l

def apply(force=0,to=None):
    #applies force to particle (does not actually move it (that happens in modernize))
    #Euler's method:
    to.dv += force*dt/to.m #Uses superposition of impulses

def project_onto_unit_vector(v=None,unit=None):
    assert v is not None and unit is not None
    #we assume used properly so that there is not a necessary check on this each time.
    return np.dot(v,unit)*unit
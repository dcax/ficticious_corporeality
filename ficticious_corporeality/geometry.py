

#this is for geometric objects and calculations that aren't strictly boundries.
from typing import Callable
import numpy as np

class Path:
    #Path in 3d space
    #Finite (I don't know how to do otherwise)
    #Defined via a paramater that ranges from 0 to 1 inclusive.
    def __init__(self, defining_function=None):
        assert defining_function is not None and isinstance(defining_function, Callable)

        self.f = defining_function
        
class ClosedPath(Path):
    #math which is linked back up and has no loose ends.
    
    @classmethod
    def make_closed_polygon_path(points=[]):
        assert len(points) != 0





    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)







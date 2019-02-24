from .utility import *

import numpy as np

#This contains paths represented as polygons.

class Path:
    #Paths (open or closed are represented as collections of points)
    def __init__(self,array):
        #Geometry of sequentially linked points
        self.points = np.asarray(array)

        self.init_pairs()
        self.init_distances()

    def init_pairs(self):
        #updates pair registry in path
        #uses self.points which is assumed to be current

        #assumes that there are at least two points.
        l = len(self)
        assert l >= 2

        self.successive_elemnt_pairs = np.empty(shape=(l-1,)+(2,))
        self.successive_elemnt_pairs[:,0] = self.points[:-1] #all but last as first node
        self.successive_elemnt_pairs[:,1] = self.points[1:] #second node is all but first

    def init_distances(self):
        pair_distance = lambda arr: dist(arr[0],arr[-1]) #gets distance between point pairs

        self.distances = np.apply_along_axis(pair_distance,axis=1,arr=self.successive_elemnt_pairs) #array of interpoint distances
        #self.distances is affected by elaboration
    
    def pairs(self):
        #gets successive element pairs (links).
        #can be found from points
        #gets total of n-1 pairs
        return self.successive_elemnt_pairs

    def __len__(self):
        #gets an object's length
        #defined as number of points
        return self.points.shape(axis=-1)

    def arclen(self):
        #Uses the euclidean norm
        #runs in O(n) for n points
        #defined as the some of all interpoint distances
        """r = 0
        pairs = self.pairs()
        l = len(pairs)
        for i in np.arange(l):
            r += dist(pairs[i,0],pairs[i,1])

        return r
        """
        
        return np.sum(self.distances)

    def elaborate(self):
        #adds points
        pass

    def shift(self):
        #shifts specific point
        pass


class ClosedPath(Path):
    #Path with the additional understanding that it is 'circular'.
    #generalises path.

    def __init__(self, array):
        super().__init__(array)

    def init_pairs(self):
        l = len(self)
        self.successive_elemnt_pairs = self.successive_elemnt_pairs.reshape((l,2))

    def pairs(self):
        #as before (this includes ciruclar pair)
        return super().pairs()

    def circumfrence(self):
        #arclength under different name
        return self.arclen()




#! /usr/bin/env python

'''
    This wavelength allocation algorithm can merely
tackle the problem whose diameter of 3D-torus topology is even
    Routing: X-Y, left-priority

    n is the radius
'''
import time
import copy
import numpy
import sys
sys.setrecursionlimit(1000000)

class BasicClass():
    def __init__(self, n):
        self.diam = 2*n
        self.radius = n
        self.links = {}
        self.dimension = 0


    def initWave(self):
        diam = self.diam
        dim  = self.dimension
        self.ringWave = numpy.zeros((diam, )*(dim*2-1), dtype=numpy.int16)
        self.wave = numpy.zeros((diam, )*(dim*2), dtype=numpy.int16)
        self.initLinks()


    #override the following two functions
    def ringToTorus(self):
        pass

    def allocWavelength(self):
        pass

#The following functions are to test the correctness
#   of this wavelength assignment algorithm.
#The allocated wavelength in every link is identical
#   and the number is equal to getMin()   
    def getMin(self):
        return int(self.diam**(self.dimension+1)/4)


    def sgn(self, m):
        if m >= 0:
            return 1
        else:
            return -1


    def isEven(self, m):
        if m % 2==0:
            return 1
        else:
            return -1


    def signal(self, dis, src, dim=-1, dest=-1):
        return self.signal_bi(dis, src, dim, dest)


    def signal_bi(self, dis, src, dim=-1, dest=-1):
        radius = self.radius
        accumulate = 0
        dimension = self.dimension
        
        if radius == abs(dis):
            if dimension == 1:
                return self.isEven(src % radius)
            
            if self.isEven(radius) == 1:
                if dim < dimension:
                    return self.isEven(dest[dim])
                return self.isEven(src[dim-1])  
            else:
                if dim == 1:
                    return self.isEven(dest[1])
                
                value = 0
                for d in range(dim):
                    value += src[d]
                return self.isEven(value)
                    
        return self.sgn(dis) * self.sgn(radius - abs(dis))

    
    def signal_uni(self, dis, src, dim=-1, dest=-1):
        if self.radius == abs(dis):
            return -1
        return self.sgn(dis) * self.sgn(self.radius - abs(dis))

    
#override the following two functions
    def initLinks(self):
        pass


    def getInitLinks(self):
        assert self.links != {}
        diam = self.diam
        links = copy.deepcopy(self.links)

        for key in links.keys():
            links[key] = set()
            
        return links
        
    @staticmethod  
    def getPath(self, src, dest):
        pass


    def addLinkWave(self, path, wavelength):
        step = len(path)
        for s in range(step-1):
            node1, node2 = path[s], path[s+1]
            link = (node1, node2)
            self.links[link].append(wavelength)
            
##            if link not in self.linksAmount:
##                link = (node2,node1)
##            self.linksAmount[link].append(wavelength)


    def toLinks(self):
        #self.initLinks()

        for src in self.coordinate():
            for dest in self.coordinate():
                path = self.getPath(src, dest)
                wavelength = self.wave[src+dest]
                self.addLinkWave(path, wavelength)

        
    def testAlgorithm(self):
        #self.initLinks()
        self.toLinks()
        
        standard = [x for x in range(self.getMin())]
        amount = self.getMin() 
        print("radix: %d, dimension: %d, Node: %d" % (self.diam, self.dimension, 2**self.dimension))
        print("wavelength: ", standard)
        #the set of wavelengths in each direction of every links    
        for value, key in self.links.items():
            try:
                assert sorted(key) == standard
            except:
                print(sorted(key))
                print(str(self.dimension) + "DTorus fails!")
                #return
            
        print(str(self.dimension) + "DTorus Pass test!")
        print("-----------------------")

    def coordinate(self):
        pass

    
    def getWave(self):
        self.allocWavelength()
        #self.testAlgorithm()
        return self.wave


    def printWave(self):
        for src in self.coordinate():
            for dest in self.coordinate():
                print((src, dest), self.wave[src+dest])
            print("---------------------")

            
    def printNode(self):
        if self.dimension == 1:
            return
        self._printNode()
        
        
    def _printNode(self):
        dest = (1,)*self.dimension
        s = []
        for src in self.coordinate():
            s.append(self.wave[src+dest])
        print(sorted(s))
        

def runTime(func):
    def _runTime():
        start = time.time()
        func()
        end = time.time()
        print("Program running time: ", end - start)
    return _runTime

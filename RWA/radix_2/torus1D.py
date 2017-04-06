#!/usr/bin/env python

'''
Notice that the algorithm can only apply to ring topology whose radix is 2.
The minimal number of wavelength is R**(d+1)/2, where d is the dimension, equals
the theoretical minimum.
'''

from basicClass import *

class Torus1D(BasicClass):
    def __init__(self, n):
        BasicClass.__init__(self, n)
        self.dimension = 1
        self.initWave()


    def allocWavelength(self):
        diam = self.diam
        radius = self.radius
        for src in range(diam):
            offset = 0
            base = (src % radius) * radius
            dest = (src + 1) % diam
            
            while dest != src:
                offset = (offset + 1) % radius
                self.wave[src][dest] = base+offset
                dest = (dest + 1) % diam


#The following functions are to test the correctness
#   of this wavelength assignment algorithm.
#The allocated wavelength in every link is identical
#   and the number is equal to getMin()
    def initLinks(self):
        diam =  self.diam
        for node in range(diam):
            self.links[(node, (node+1)%diam)] = []
            

    def getPath(self, src, dest):
        path = []
        diam = self.diam

        dis = dest - src
        sign = self.signal(dis, src)
        node = src
        if dis != 0:
            while node != dest:
                path.append(node)
                node = (node + sign) % diam

        assert node == dest
        path.append(dest)
        return path


    def toLinks(self):
        diam = self.diam
        radius = self.radius
        for src in range(diam):
            for dest in range(diam):
                self.addLinkWave(self.getPath(src, dest),
                            self.wave[src][dest])


    def printWave(self):
        diam = self.diam
        for src in range(diam):
            for dest in range(diam):
                print((src, dest), self.wave[src][dest])
            print('---------------')

       
@runTime
def main():
    radius = 1
    ring = Torus1D(radius)
    ring.getWave()
    

if __name__ == "__main__":
    main()


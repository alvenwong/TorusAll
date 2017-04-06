#! /usr/bin/env python

'''
Notice that the algorithm can only apply to ring topology whose radix is 2.
The minimal number of wavelength is R**(d+1)/2, where d is the dimension, equals
the theoretical minimum.
'''
from basicClass import *
from torus1D import Torus1D

class Torus2D(BasicClass):
    def __init__(self, n):
        BasicClass.__init__(self, n)
        self.dimension = 2
        self.initWave()
        
                     
    def ringToTorus(self):
        diam = self.diam
        radius = self.radius
        self.Torus1D = Torus1D(radius)
        self.torus1DWave = self.Torus1D.getWave()
        
        flag = 0
        ringPos = radius
        for src in range(0, diam):
            for dest in range(0, diam):
                flag = 0
                    
                if src == dest:
                    base = (src%radius)*2*radius*radius
                    #y axis
                    for y in range(diam):
                        if y < ringPos:
                            self.ringWave[src][dest][y] = base + (y%radius)*2
                        else:
                            self.ringWave[src][dest][y] = base + (y%radius)*2 + 1
                    continue
                            
                if (dest+diam-src)%diam >= radius:
                    flag = 1
                    
                base = self.torus1DWave[src][dest] * diam
                #y axis
                for y in range(diam):
                    if y < ringPos:
                        self.ringWave[src][dest][y] = base + (y%radius)*2 + flag
                    else:
                        self.ringWave[src][dest][y] = base + (y%radius)*2 + (flag+1)%2

    
    def allocWavelength(self):
        self.ringToTorus()
        
        diam = self.diam
        radius = self.radius
        
        for src_x, src_y in self.coordinate():
            offset = radius - src_y
            for dest_x, dest_y in self.coordinate():
                self.wave[src_x][src_y][dest_x][dest_y]\
                    = self.ringWave[(src_x-offset)%diam][(dest_x-offset)%diam][dest_y]
    

#   The following functions are to test the correctness
#of this wavelength assignment algorithm.
#   The allocated wavelength in every link is identical
#and the number is equal to getMin()
    def initLinks(self):
        diam = self.diam

        for x, y in self.coordinate():
            self.links[((x,y), ((x+1)%diam,y))] = []
            self.links[((x,y), (x,(y+1)%diam))] = []

    
    def getPath(self, src, dest):
        diam = self.diam
        radius = self.radius
        path = []
        x_dest, y_dest = dest[0], dest[1]
        x_src, y_src = src[0], src[1]
        
        x_dis = x_dest - x_src
        y_dis = y_dest - y_src

        #x axis
        if(x_dis != 0):
            x_signal = self.signal(x_dis, src, 1, dest)
            x_src_tmp = x_src
            while(x_src_tmp != x_dest):
                path.append((x_src_tmp, y_src))
                x_src_tmp = (x_src_tmp + x_signal + diam) % diam

        #y axis
        if(y_dis != 0):
            y_signal = self.signal(y_dis, src, 2, dest)
            y_src_tmp = y_src
            while(y_src_tmp != y_dest):
                path.append((x_dest, y_src_tmp))
                y_src_tmp = (y_src_tmp + y_signal + diam) % diam
                   
        path.append((x_dest, y_dest))
        return path


    def coordinate(self):
        diam = self.diam
        for x in range(diam):
            for y in range(diam):
                yield x, y


@runTime
def main():
    radius = 1
    torus2D = Torus2D(radius)
    torus2D.getWave()


if __name__ == "__main__":
    main()
    

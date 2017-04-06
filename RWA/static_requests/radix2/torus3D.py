#! /usr/bin/env python

'''
    This wavelength allocation algorithm can merely
tackle the problem whose diameter of 3D-torus topology is even
    Routing: X-Y, left-priority

    n is the radius
'''
from basicClass import *
from torus2D import Torus2D

class Torus3D(BasicClass):
    def __init__(self, n):
        BasicClass.__init__(self, n)
        self.dimension = 3
        self.initWave()
         

    def ringToTorus(self):
        diam = self.diam
        radius = self.radius
        self.Torus2D = Torus2D(radius)
        self.torus2DWave = self.Torus2D.getWave()
        waveRecord = []
        flag = 0
        ringPos = radius

        for dest_x, dest_y in self.Torus2D.coordinate():
            assert waveRecord == []
            for src_x, src_y in self.Torus2D.coordinate():
                flag = 0
        
                wave = self.torus2DWave[src_x][src_y][dest_x][dest_y]
                base = wave * diam
                if wave not in waveRecord:
                    flag = 0
                    waveRecord.append(wave)
                else:
                    flag = 1
                    waveRecord.remove(wave)
                    
                #z axis
                for z in range(diam):
                    if z < ringPos:
                        self.ringWave[src_x][src_y][dest_x][dest_y][z]\
                            = base + (z%radius)*2 + flag
                    else:
                        self.ringWave[src_x][src_y][dest_x][dest_y][z]\
                            = base + (z%radius)*2 + (flag+1)%2


    def allocWavelength(self):
        self.ringToTorus()
                
        diam = self.diam
        radius = self.radius

        for src_x, src_y, src_z in self.coordinate():
            offset = radius - src_z
            for dest_x, dest_y, dest_z in self.coordinate():        
                self.wave[src_x][src_y][src_z][dest_x][dest_y][dest_z] \
                    = self.ringWave[src_x][(src_y-offset)%diam][dest_x][(dest_y-offset)%diam][dest_z] 


#   The following functions are to test the correctness
#of this wavelength assignment algorithm.
#   The allocated wavelength in every link is identical
#and the number is equal to getMin()
    def initLinks(self):
        diam = self.diam

        for x, y, z in self.coordinate():
            self.links[((x,y,z), ((x+1)%diam,y,z))] = []
            self.links[((x,y,z), (x,(y+1)%diam,z))] = []
            self.links[((x,y,z), (x,y,(z+1)%diam))] = []

    
    def getPath(self, src, dest):
        diam = self.diam
        radius = self.radius
        path = [] 
        x_dest, y_dest, z_dest = dest[0], dest[1], dest[2]
        x_src, y_src, z_src = src[0], src[1], src[2]
        
        x_dis = x_dest - x_src
        y_dis = y_dest - y_src
        z_dis = z_dest - z_src

        #x axis
        if(x_dis != 0):
            x_signal = self.signal(x_dis, src, 1, dest)
            x_src_tmp = x_src
            while(x_src_tmp != x_dest):
                path.append((x_src_tmp, y_src, z_src))
                x_src_tmp = (x_src_tmp + x_signal + diam) % diam
                
        #y axis
        if(y_dis != 0):
            y_signal = self.signal(y_dis, src, 2, dest)
            y_src_tmp = y_src
            while(y_src_tmp != y_dest):
                path.append((x_dest, y_src_tmp, z_src))
                y_src_tmp = (y_src_tmp + y_signal + diam) % diam

        #z axis
        if(z_dis != 0):
            z_signal = self.signal(z_dis, src, 3, dest)
            z_src_tmp = z_src
            while(z_src_tmp != z_dest):
                path.append((x_dest, y_dest, z_src_tmp))
                z_src_tmp = (z_src_tmp + z_signal + diam) % diam
             
        path.append((x_dest, y_dest, z_dest))
        return path
        

    def coordinate(self):
        diam = self.diam
        for x in range(diam):
            for y in range(diam):
                for z in range(diam):
                    yield x, y, z
                
    
@runTime    
def main():
    radius = 1
    torus3D = Torus3D(radius)
    torus3D.getWave()


if __name__ == "__main__":
    main()

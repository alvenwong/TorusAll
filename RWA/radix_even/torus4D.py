#! /usr/bin/env python

'''
    This wavelength allocation algorithm can merely
tackle the problem whose diameter of 4D-torus topology is even
    Routing: X-Y, left-priority

    n is the radius
'''
from basicClass import *
from torus3D import Torus3D

class Torus4D(BasicClass):
    def __init__(self, n):
        BasicClass.__init__(self, n)
        self.dimension = 4
        self.initWave()
        self.Torus3D = Torus3D(n)


    def ringToTorus(self):
        diam = self.diam
        radius = self.radius        
        self.torus3DWave = self.Torus3D.getWave()
        waveRecord = []
        flag = 0
        ringPos = radius

        for dest_x, dest_y, dest_z in self.Torus3D.coordinate():
            assert waveRecord == []
            for src_x, src_y, src_z in self.Torus3D.coordinate():
                flag = 0
        
                wave = self.torus3DWave[src_x][src_y][src_z][dest_x][dest_y][dest_z]
                base = wave * diam
                if wave not in waveRecord:
                    flag = 0
                    waveRecord.append(wave)
                else:
                    flag = 1
                    waveRecord.remove(wave)
                    
                #u axis
                for u in range(diam):
                    if u < ringPos:
                        self.ringWave[src_x][src_y][src_z][dest_x][dest_y][dest_z][u]\
                            = base + (u%radius)*2 + flag
                    else:
                        self.ringWave[src_x][src_y][src_z][dest_x][dest_y][dest_z][u]\
                            = base + (u%radius)*2 + (flag+1)%2


    def allocWavelength(self):
        self.ringToTorus()
                
        diam = self.diam
        radius = self.radius

        for src_x, src_y, src_z, src_u in self.coordinate():
            offset = radius - src_u
            for dest_x, dest_y, dest_z, dest_u in self.coordinate():        
                self.wave[src_x][src_y][src_z][src_u][dest_x][dest_y][dest_z][dest_u] \
                    = self.ringWave[src_x][src_y][(src_z-offset)%diam][dest_x][dest_y][(dest_z-offset)%diam][dest_u] 


#The following functions are to test the correctness
#   of this wavelength assignment algorithm.
#The allocated wavelength in every link is identical
#   and the number is equal to getMin()
    def initLinks(self):
        diam = self.diam

        #x axis
        for y, z, u, x in self.coordinate():
            self.links[((x,y,z,u), ((x+1)%diam,y,z,u))] = []
            self.links[(((x+1)%diam,y,z,u), (x,y,z,u))] = []

            self.linksAmount[((x,y,z,u), ((x+1)%diam,y,z,u))] = []

        #y axis
        for x, z, u, y in self.coordinate():
            self.links[((x,y,z,u), (x,(y+1)%diam,z,u))] = []
            self.links[((x,(y+1)%diam,z,u), (x,y,z,u))] = []

            self.linksAmount[((x,y,z,u), (x,(y+1)%diam,z,u))] = []
                        
        #z axis
        for x, y, u, z in self.coordinate():
            self.links[((x,y,z,u), (x,y,(z+1)%diam,u))] = []
            self.links[((x,y,(z+1)%diam,u), (x,y,z,u))] = []

            self.linksAmount[((x,y,z,u), (x,y,(z+1)%diam,u))] = []

        #u axis
        for x, y, z, u in self.coordinate():
            self.links[((x,y,z,u), (x,y,z,(u+1)%diam))] = []
            self.links[((x,y,z,(u+1)%diam), (x,y,z,u))] = []

            self.linksAmount[((x,y,z,u), (x,y,z,(u+1)%diam))] = []
                    
    
    def getPath(self, src, dest):
        diam = self.diam
        radius = self.radius
        path = [] 
        x_dest, y_dest, z_dest, u_dest = dest[0], dest[1], dest[2], dest[3]
        x_src, y_src, z_src, u_src = src[0], src[1], src[2], src[3]
        
        x_dis = x_dest - x_src
        y_dis = y_dest - y_src
        z_dis = z_dest - z_src
        u_dis = u_dest - u_src

        #x axis
        if(x_dis != 0):
            x_signal = self.signal(x_dis, src, 1, dest)
            x_src_tmp = x_src
            while(x_src_tmp != x_dest):
                path.append((x_src_tmp, y_src, z_src, u_src))
                x_src_tmp = (x_src_tmp + x_signal + diam) % diam
                
        #y axis
        if(y_dis != 0):
            y_signal = self.signal(y_dis, src, 2, dest)
            y_src_tmp = y_src
            while(y_src_tmp != y_dest):
                path.append((x_dest, y_src_tmp, z_src, u_src))
                y_src_tmp = (y_src_tmp + y_signal + diam) % diam

        #z axis
        if(z_dis != 0):
            z_signal = self.signal(z_dis, src, 3, dest)
            z_src_tmp = z_src
            while(z_src_tmp != z_dest):
                path.append((x_dest, y_dest, z_src_tmp, u_src))
                z_src_tmp = (z_src_tmp + z_signal + diam) % diam

        #u axis
        if(u_dis != 0):
            u_signal = self.signal(u_dis, src, 4, dest)
            u_src_tmp = u_src
            while(u_src_tmp != u_dest):
                path.append((x_dest, y_dest, z_dest, u_src_tmp))
                u_src_tmp = (u_src_tmp + u_signal + diam) % diam
             
        path.append((x_dest, y_dest, z_dest, u_dest))
        return path
        

    def coordinate(self):
        diam = self.diam
        for x in range(diam):
            for y in range(diam):
                for z in range(diam):
                    for u in range(diam):
                        yield x, y, z, u

    
@runTime    
def main():
    radius = int(input("input the radius of 4D torus:\n>>> "))
    torus4D = Torus4D(radius)
    torus4D.getWave()


if __name__ == "__main__":
    main()

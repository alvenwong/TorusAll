#! /usr/bin/env python

'''
    This wavelength allocation algorithm can merely
tackle the problem whose diameter of 5D-torus topology is even
    Routing: X-Y, left-priority

    n is the radius
'''
from basicClass import *
from torus5D import Torus5D
import copy

class Torus6D(BasicClass):
    def __init__(self, n):
        BasicClass.__init__(self, n)
        self.dimension = 6
        self.initWave()


    def ringToTorus(self):
        diam = self.diam
        radius = self.radius
        self.Torus5D = Torus5D(radius)
        self.torus5DWave = self.Torus5D.getWave()
        waveRecord = []
        flag = 0
        ringPos = radius

        for dest_x, dest_y, dest_z, dest_u, dest_v in self.Torus5D.coordinate():
            assert waveRecord == []
            for src_x, src_y, src_z, src_u, src_v in self.Torus5D.coordinate():
                flag = 0
        
                wave = self.torus5DWave[src_x][src_y][src_z][src_u][src_v][dest_x][dest_y][dest_z][dest_u][dest_v]
                base = wave * diam
                if wave not in waveRecord:
                    flag = 0
                    waveRecord.append(wave)
                else:
                    flag = 1
                    waveRecord.remove(wave)
                    
                #v axis
                for w in range(diam):
                    if w < ringPos:
                        self.ringWave[src_x][src_y][src_z][src_u][src_v][dest_x][dest_y][dest_z][dest_u][dest_v][w]\
                            = base + (w % radius)*2 + flag
                    else:
                        self.ringWave[src_x][src_y][src_z][src_u][src_v][dest_x][dest_y][dest_z][dest_u][dest_v][w]\
                            = base + (w % radius)*2 + (flag+1)%2


    def allocWavelength(self):
        self.ringToTorus()
                
        diam = self.diam
        radius = self.radius

        for src_x, src_y, src_z, src_u, src_v, src_w in self.coordinate():
            offset = radius - src_w
            for dest_x, dest_y, dest_z, dest_u, dest_v, dest_w in self.coordinate():        
                self.wave[src_x][src_y][src_z][src_u][src_v][src_w][dest_x][dest_y][dest_z][dest_u][dest_v][dest_w] \
                    = self.ringWave[src_x][src_y][src_z][src_u][(src_v-offset)%diam][dest_x][dest_y][dest_z][dest_u][(dest_v-offset)%diam][dest_w] 


#The following functions are to test the correctness
#   of this wavelength assignment algorithm.
#The allocated wavelength in every link is identical
#   and the number is equal to getMin()
    def initLinks(self):
        diam = self.diam

        for x, y, z, u, v, w in self.coordinate():
            self.links[((x,y,z,u,v,w), ((x+1)%diam,y,z,u,v,w))] = []
            self.links[((x,y,z,u,v,w), (x,(y+1)%diam,z,u,v,w))] = []
            self.links[((x,y,z,u,v,w), (x,y,(z+1)%diam,u,v,w))] = []
            self.links[((x,y,z,u,v,w), (x,y,z,(u+1)%diam,v,w))] = []
            self.links[((x,y,z,u,v,w), (x,y,z,u,(v+1)%diam,w))] = []
            self.links[((x,y,z,u,v,w), (x,y,z,u,v,(w+1)%diam))] = []
    
    
    def getPath(self, src, dest):
        diam = self.diam
        radius = self.radius
        path = [] 
        x_dest, y_dest, z_dest, u_dest, v_dest, w_dest = dest[0], dest[1], dest[2], dest[3], dest[4], dest[5]
        x_src, y_src, z_src, u_src, v_src, w_src = src[0], src[1], src[2], src[3], src[4], src[5]
        
        x_dis = x_dest - x_src
        y_dis = y_dest - y_src
        z_dis = z_dest - z_src
        u_dis = u_dest - u_src
        v_dis = v_dest - v_src
        w_dis = w_dest - w_src

        #x axis
        if(x_dis != 0):
            x_signal = self.signal(x_dis, src, 1, dest)
            x_src_tmp = x_src
            while(x_src_tmp != x_dest):
                path.append((x_src_tmp, y_src, z_src, u_src, v_src, w_src))
                x_src_tmp = (x_src_tmp + x_signal + diam) % diam
                
        #y axis
        if(y_dis != 0):
            y_signal = self.signal(y_dis, src, 2, dest)
            y_src_tmp = y_src
            while(y_src_tmp != y_dest):
                path.append((x_dest, y_src_tmp, z_src, u_src, v_src, w_src))
                y_src_tmp = (y_src_tmp + y_signal + diam) % diam

        #z axis
        if(z_dis != 0):
            z_signal = self.signal(z_dis, src, 3, dest)
            z_src_tmp = z_src
            while(z_src_tmp != z_dest):
                path.append((x_dest, y_dest, z_src_tmp, u_src, v_src, w_src))
                z_src_tmp = (z_src_tmp + z_signal + diam) % diam

        #u axis
        if(u_dis != 0):
            u_signal = self.signal(u_dis, src, 4, dest)
            u_src_tmp = u_src
            while(u_src_tmp != u_dest):
                path.append((x_dest, y_dest, z_dest, u_src_tmp, v_src, w_src))
                u_src_tmp = (u_src_tmp + u_signal + diam) % diam

        #v axis
        if(v_dis != 0):
            v_signal = self.signal(v_dis, src, 5, dest)
            v_src_tmp = v_src
            while(v_src_tmp != v_dest):
                path.append((x_dest, y_dest, z_dest, u_dest, v_src_tmp, w_src))
                v_src_tmp = (v_src_tmp + v_signal + diam) % diam

        #w axis
        if(w_dis != 0):
            w_signal = self.signal(w_dis, src, 6, dest)
            w_src_tmp = w_src
            while(w_src_tmp != w_dest):
                path.append((x_dest, y_dest, z_dest, u_dest, v_dest, w_src_tmp))
                w_src_tmp = (w_src_tmp + w_signal + diam) % diam
             
        path.append((x_dest, y_dest, z_dest, u_dest, v_dest, w_dest))
        return path
        

    def coordinate(self):
        diam = self.diam
        
        for x in range(diam):
            for y in range(diam):
                for z in range(diam):
                    for u in range(diam):
                        for v in range(diam):
                            for w in range(diam):
                                yield x, y, z, u, v, w

    
@runTime    
def main():
    radius = 1
    torus6D = Torus6D(radius)
    torus6D.getWave()


if __name__ == "__main__":
    main()

#-------------------------------------------------------------------------------
# Name:        RWA
# Purpose:
#
# Author:      alven
#
# Created:     23/09/2015
# Copyright:   (c) alven 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pulp
import itertools
from requests import Requests

radix = 1
dimension = 3
limit = 3

class Paths():
    def __init__(self, radius, dimension, requestsPool, limit):
        self.radius = radius
        self.diameter = radius * 2
        self.dimension = dimension
        self.nodes = (radius*2) ** dimension
        self.requestsPool = requestsPool
        self.limit = limit

    #just for radix=1
    def getPath(self, src, dest):
        assert isinstance(src, tuple)
        assert isinstance(dest, tuple)
        path = list()

        differ = list()
        for dim in range(self.dimension):
            if src[dim] != dest[dim]:
                differ.append(dim)

        pathsPool = list(itertools.permutations(differ, len(differ)))

        for permutation in pathsPool:
            path.clear()
            path.append(src)
            tempSrc = list(src)
            #an alternate path
            for index in permutation:
                tempSrc[index] ^= 1
                path.append(tuple(tempSrc))

            yield path


    def getPathPool(self, src, dest):
        paths = []
        f = self.getPath(self.node2Coordinate(src), self.node2Coordinate(dest))
        try:
            for num in range(self.limit):
                path = next(f)
                paths.append(path)
        except:
            pass

        return paths


    def getPathsPool(self):
        pathsPool = {}
        for src in range(self.nodes):
            for dest in self.requestsPool[src]:
                pathsPool[(src, dest)] = self.getPathPool(src, dest)

        return pathsPool


    def node2Coordinate(self, node):
        if self.dimension == 1:
            return node

        dim = self.dimension
        dia = self.diameter
        coor = ()
        while dim != 0:
            c = node%dia
            node = int(node/dia)
            coor += (c,)
            dim -= 1

        if node > 0:
            print("node is out of range!")
            return -1

        return coor


    def coordinate2Node(self, coor):
        if self.dimension == 1:
            return coor
        assert isinstance(coor, tuple)
        node = 0
        dim = len(coor)
        dim -= 1
        dia = self.diameter
        while dim >= 0:
            if coor[dim] >= dia:
                print("index is out of range!")
                return -1
            node = node*dia + coor[dim]
            dim -= 1

        return node


def main():
    requests = Requests(radix, dimension, 0.5)
    requests.generateRequest()
    requestsPool = requests.getRequest()

    paths = Paths(radix, dimension, requestsPool, limit)
    pathsPool = paths.getPathsPool()

    for key, value in pathsPool.items():
        print(key, value)


if __name__ == '__main__':
    main()

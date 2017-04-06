#! /usr/bin/env python

import sys
radix = '2'
sys.path.append(sys.path[0]+"\\radix"+radix)

from requests import Requests
import random
from timer import Time
from RWA import RWA
import pdb
file = "results.txt"

class Assignment():
    def __init__(self, radius, dimension, requestRate, adaptive, WAName):
        self.period = 200
        self.static = 0
        self.dynamic = 1
        self.fixed = 0
        self.radius = radius
        self.diameter = self.radius * 2
        self.dimension = dimension
        self.requestRate = requestRate
        self.nodes = (self.radius * 2) ** self.dimension
        self.holdingTime = 5
        self.connectionFailPool = [[] for node in range(self.nodes)]

        self.isORWA = 0
        #self.routingName = "Adaptive Routing"
        self.routingName = "Fixed Routing"
        self.WAName = WAName

        self.requestsCounter = 0
        self.blockingCounter = 0
        self.clock = Time()
        self.RWA = RWA(self.isORWA, self.radius, self.dimension, adaptive)
        self.chooseAlgorithm(self.isORWA, self.routingName, self.WAName)


    def clear(self):
        for node in range(self.nodes):
            self.connectionFailPool[node].clear()


    def chooseAlgorithm(self, isORWA, routing, WA):
        if isORWA == 1:
            self.assignment = self.ORWA
        else:
            self.assignment = self.RoutingWavelengthAssignment
            self.rwa = self.RWA.rwa

            if WA == "First Fit":
                self.WA = self.RWA.firstFit
            elif WA == "Least Used":
                self.WA = self.RWA.leastUsed
            elif WA == "Most Used":
                self.WA = self.RWA.mostUsed
            elif WA == "Random wavelength assignment":
                self.WA = self.RWA.randomWA


    def getRequestsNum(self, requestPool):
        counter = 0
        for node in range(self.nodes):
            counter += len(requestPool[node])

        return counter


    def evaluate(self):
        requests = Requests(self.radius, self.dimension,
                            self.fixed, self.requestRate)
        requests.setHoldingTime(self.holdingTime)

        while self.clock.getTime() < self.period:
            self.clear()
            requests.generateRequest(self.clock.getTime())
            requestPool = requests.getRequest()
            self.requestsCounter += self.getRequestsNum(requestPool)
            blockingNum = self.assignment(requestPool)
            requests.deleteFailure(self.connectionFailPool)
            self.clock.addTime()
            self.blockingCounter += blockingNum
            #delete outdated connections
            self.RWA.deleteRecordPool(self.clock.getTime())

        blockingRate = self.blockingCounter/self.requestsCounter
        print(self.requestRate, self.requestsCounter, self.blockingCounter, blockingRate)


    #the routing and wavelength assignment we propose, O stands for optimal
    def ORWA(self, requestPool):
        blockingNum = 0
        for node in range(self.nodes):
            for key, value in requestPool[node].items():
                src = self.node2Coordinate(node)
                dest = self.node2Coordinate(key)
                blockingNum += self.RWA.ORWA(src, dest, value)

        return blockingNum


    def RoutingWavelengthAssignment(self, requestPool, shuffle = 0):
        blockingNum = 0
        nodeSet = [node for node in range(self.nodes)]
        if shuffle != 0:
            random.shuffle(nodeSet)

        for node in nodeSet:
            for key, value in requestPool[node].items():
                src = self.node2Coordinate(node)
                dest = self.node2Coordinate(key)
                blocking = self.rwa(src, dest, value, self.routingName, self.WA)
                if blocking == 1:
                    self.connectionFailPool[node].append(key)
                    blockingNum += blocking

        return blockingNum


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
    radius = 1
    dimension = 6
    step = 1/64

    old = sys.stdout

    adaptive = 0

    ListWA = ["Most Used","Random wavelength assignment"]
    for WA in ListWA:
        f = open(WA+file, 'w')
        sys.stdout = f
        requestRate = 1/64
        while requestRate < 1:
            assign = Assignment(radius, dimension, requestRate, adaptive, WA)
            assign.evaluate()
            requestRate += step
        f.close()


    sys.stdout = old


if __name__ == "__main__":
    main()







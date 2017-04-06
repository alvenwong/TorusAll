#! /usr/bin/env python

import sys

from random import randint

#maximum holding time
MAX = 20
MIN = 5

class Requests():
    def __init__(self, radius, dimension, fixed, requestRate):
        self.radius = radius
        self.diam = radius * 2
        self.dimension = dimension
        self.nodes = (radius*2) ** dimension
        #self.static = static
        self.maxHoldingTime = MAX
        self.minHoldingTime = MIN
        self.requestRate = requestRate
        self.initParams()
        self.fixedHoldingTime = fixed
        

    def initParams(self):
        self.connectionPool = [{} for node in range(self.nodes)]
        self.tempPool = [{} for node in range(self.nodes)]
        assert self.requestRate <= 1
        if self.requestRate == 1:
            self.requestNum = self.nodes -1
        else:
            self.requestNum = int(self.requestRate * self.nodes)


    def setHoldingTime(self, holdingTime):
        self.holdingTime = holdingTime


    def getRandomHoldingTime(self):
        return randint(self.minHoldingTime, self.maxHoldingTime)


    def getHoldingTime(self):
        if self.fixedHoldingTime == 1:
            return self.holdingTime
        return self.getRandomHoldingTime()


    def randomDest(self, src):
        nodes = self.nodes
        while True:
            dest = randint(0, nodes-1)
            if dest != src:
                return dest


    def getDest(self, src):
        return self.randomDest(src)


    def deleteFailure(self, connectionFailPool):
        for node in range(self.nodes):
            for dest in connectionFailPool[node]:
                self.connectionPool[node].pop(dest)
        

    def releaseConnection(self, time):
        for node in range(self.nodes):
            deleteList = []
            #release connection
            for key, value in self.connectionPool[node].items():
                if value == time:
                    assert key not in deleteList
                    deleteList.append(key)

            for key in deleteList:
                self.connectionPool[node].pop(key)


    def generateRequest(self, time):
        self.releaseConnection(time)
        for node in range(self.nodes):
            self.tempPool[node].clear()
        
        for node in range(self.nodes):
            while len(self.connectionPool[node]) < self.requestNum:
                dest = self.getDest(node)
                releaseTime = self.getHoldingTime() + time
                if dest not in self.connectionPool[node]:
                    self.connectionPool[node][dest] = releaseTime
                    self.tempPool[node][dest] = releaseTime
                    

    def getRequest(self):
        return self.tempPool


def main():
    requests  = Requests(1, 4, 0, 0.5)
    requests.setHoldingTime(5)
    requests.generateRequest()
    pool = requests.getRequest()
    for node in range(16):
        print(pool[node])

if __name__ == "__main__":
    main()

        

        



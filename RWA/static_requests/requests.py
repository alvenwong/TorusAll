#! /usr/bin/env python

from random import randint

#generate static connection requests

class Requests():
    def __init__(self, radius, dimension, requestRate, fixed=0):
        self.radius = radius
        self.diam = radius * 2
        self.dimension = dimension
        self.nodes = (radius*2) ** dimension
        self.requestRate = requestRate
        self.initParams()


    def initParams(self):
        self.connectionPool = [[] for node in range(self.nodes)]
        assert self.requestRate <= 1
        if self.requestRate == 1:
            self.requestNum = self.nodes -1
        else:
            self.requestNum = int(self.requestRate * self.nodes)


    def randomDest(self, src):
        nodes = self.nodes
        while True:
            dest = randint(0, nodes-1)
            if dest != src:
                return dest


    def getDest(self, src):
        return self.randomDest(src)


    def generateRequest(self):
        for src in range(self.nodes):
            while len(self.connectionPool[src]) < self.requestNum:
                dest = self.getDest(src)
                if dest not in self.connectionPool[src]:
                    self.connectionPool[src].append(dest)


    def getRequest(self):
        return self.connectionPool
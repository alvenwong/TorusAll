#! /usr/bin/env python

import itertools
import copy
from torus6D import Torus6D as Torus
import pdb
from sys import maxsize as MAXINT
from random import randint

class RWA():
    def __init__(self, ORWA, radius, dimension, adaptive=0):
        self.radius = radius
        self.dimension = dimension
        self.torus = Torus(self.radius)
        self.nodes = (radius * 2) ** dimension
        self.links = self.torus.getInitLinks()
        self.wavelengthNum = 32
        self.adaptive = adaptive

        if ORWA == 1:
            self.wave = self.torus.getWave()
        else:
            self.setLinkCapacity()

        self.recordPool = dict()


    def setLinkCapacity(self):
        self.capacity = set()
        for w in range(self.wavelengthNum):
            self.capacity.add(w)

    #optimal routing and wavelength assignment
    def ORWA(self, src, dest, endingTime):
        wavelength = self.wave[src+dest]
        path = self.torus.getPath(src, dest)
        blocking = self.addLinkWave(path, wavelength, endingTime)

        return blocking


    def getLink(self, node1, node2):
        if (node1, node2) in self.links:
            return (node1, node2)
        return (node2, node1)


    def addLinkWave(self, path, wavelength, endingTime):
        step = len(path)

        #if ORWA, the next six lines of code are used to test if
        #wavelength contention occurs
##        for s in range(step-1):
##            node1, node2 = path[s], path[s+1]
##            link = (node1, node2)
##            if wavelength in self.links[link]:
##                #pdb.set_trace()
##                return 1

        for s in range(step-1):
            node1, node2 = path[s], path[s+1]
            link = self.getLink(node1, node2)
            self.links[link].add(wavelength)

        self.insectRecordPool(endingTime, path, wavelength)
        return 0


    def deleteLinkWave(self, path, wavelength):
        step = len(path)
        for s in range(step-1):
            node1, node2 = path[s], path[s+1]
            link = self.getLink(node1, node2)
            assert wavelength in self.links[link]
            self.links[link].remove(wavelength)


    def insectRecordPool(self, endingTime, path, wavelength):
        try:
            self.recordPool[endingTime].append((path, wavelength))
        except:
            self.recordPool[endingTime] = [(path, wavelength)]


    def deleteRecordPool(self, time):
        try:
            deletePool = self.recordPool.pop(time)
            for pair in deletePool:
                self.deleteLinkWave(pair[0], pair[1])
        except:
            pass


    def rwa(self, src, dest, endingTime, routing, WA):
        if routing == "Fixed Routing":
            path = self.fixedRouting(src, dest)
            minWave, freeWave = WA(path)
            if minWave == -1:
                return 1
            self.addLinkWave(path, minWave, endingTime)
            return 0

        elif routing == "Adaptive Routing":
            paths = self.adaptiveRouting(src, dest)
            maxFreeWave = 0
            minWave = self.wavelengthNum
            optimalPath = list()
            for path in paths:
                wave, freeWave = WA(path)
                #three adaptive routing algorithms
                if self.adaptive == 0:
                    if wave == -1:
                        continue
                    optimalPath = path
                    minWave = wave
                    break

                elif self.adaptive == 1:
                    if freeWave > maxFreeWave:
                        maxFreeWave = freeWave
                        optimalPath = copy.deepcopy(path)
                        minWave = wave

                elif self.adaptive == 2:
                    if 0 <= wave < minWave:
                        optimalPath = copy.deepcopy(path)
                        minWave = wave

            if minWave == self.wavelengthNum:
                return 1

            self.addLinkWave(optimalPath, minWave, endingTime)
            return 0


    #Routing Algorithm
    def fixedRouting(self, src, dest):
        # x-y routing
        return self.torus.getPath(src, dest)


    def adaptiveRouting(self, src, dest):
        #just for radix=2
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


    def getAvailableWave(self, path):
        step = len(path)
        capacity = copy.deepcopy(self.capacity)
        remainder = capacity

        for s in range(step-1):
            node1, node2 = path[s], path[s+1]
            link = self.getLink(node1, node2)
            remainder &= (capacity - self.links[link])
            if len(remainder) == 0:
                return -1

        return remainder


    #Wavelength Assignment
    def firstFit(self, path):
        remainder = self.getAvailableWave(path)
        if remainder == -1:
            return -1, -1

        minWave = self.wavelengthNum
        for item in remainder:
            if minWave > item:
                minWave = item

        return minWave, len(remainder)


    #calculate the number of links containing wave
    def waveCounter(self, wave):
        counter  = 0
        for waveSet in self.links.values():
            if wave in waveSet:
                counter += 1

        return counter


    def leastUsed(self, path):
        remainder = self.getAvailableWave(path)
        if remainder == -1:
            return -1, -1

        minCounter = MAXINT

        wave = self.wavelengthNum
        for item in remainder:
            counter = self.waveCounter(item)
            if minCounter > counter:
                minCounter = counter
                wave = item

        assert wave != self.wavelengthNum
        return wave, len(remainder)


    def mostUsed(self, path):
        remainder = self.getAvailableWave(path)
        if remainder == -1:
            return -1, -1

        maxCounter = -1
        wave = MAXINT

        for item in remainder:
            counter = self.waveCounter(item)
            if maxCounter < counter:
                maxCounter = counter
                wave = item

        assert wave != MAXINT
        return wave, len(remainder)


    def randomWA(self, path):
        remainder = self.getAvailableWave(path)
        if remainder == -1:
            return -1, -1

        listRemainder = list(remainder)
        length = len(listRemainder)
        index = randint(0, length-1)

        return listRemainder[index], length
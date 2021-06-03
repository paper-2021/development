from collections import deque
import heapq
from haversine import haversine
import time

idCounter = 0

class Edge:
    def __init__(self, weight, traffic, node):
        self.weight = weight
        self.traffic = traffic
        self.node = node

class Node():
    parent = None
    
    f = 0; 
    g = 0; 
    
    def __init__(self, latitude, longitude):
        global idCounter
        idCounter = idCounter + 1
        self.latitude = latitude
        self.longitude = longitude
        self.id = idCounter
        self.neighbors = []
        self.parent = None
        self.f = 0
        self.g = 0

    def __str__(self):
        return  ("Node " + str(self.id))
    
    def __repr__(self):
        return  ("Node " + str(self.id))
    
    def __gt__(self, other):
        return (self.f).__gt__(other.f)

    def addBranch(self, weight, traffic, node):
        newEdge = Edge(weight, traffic, node)
        self.neighbors.append(newEdge)

    def changeBranch(self, traffic, node) :
        for neighbor in self.neighbors :
            if(neighbor.node == node) :
                neighbor.traffic = traffic
                break
    
    def calculateHeuristic(self, target):
        return haversine((self.longitude, self.latitude), (target.longitude, target.latitude)) * 10

    def aStar(self, start, target):
        closedList = []
        openList = []
        start.f = start.g + start.calculateHeuristic(target)
        heapq.heappush(openList, start)
        while(openList != 0):
            n = openList[0]
            
            if(n == target):
                return n
            for edge in n.neighbors:
                m = edge.node
                totalWeight = n.g + edge.weight/edge.traffic
                if(m not in openList and m not in closedList):
                    m.parent = n
                    m.g = totalWeight
                    m.f = m.g + m.calculateHeuristic(target)
                    heapq.heappush(openList, m)
                else:
                    if(totalWeight < m.g):
                        m.parent = n
                        m.g = totalWeight
                        m.f = m.g + m.calculateHeuristic(target)
                        if(m in closedList):
                            closedList.remove(m)
                            heapq.heappush(openList, m)
            openList.remove(n)
            heapq.heappush(closedList, n)
        return None

    def printPath(self, target):
        n = target
        if n == None:
            return ' '
        ids = []
        while(n.parent != None):
            ids.append(n.id)
            n = n.parent
        ids.append(n.id)
        ids = reversed(ids)

        route = []
        for i in ids:
            route.append(i)
        return route
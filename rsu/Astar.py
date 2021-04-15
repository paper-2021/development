from collections import deque
import heapq

idCounter = -1

class Edge:
        def __init__(self, weight, node):
            self.weight = weight
            self.node = node
class Node():
    
    # Id for readability of result purposes
     #private static int 
    
    # Parent in the path
    parent = None # public Node , null
    
    # Evaluation functions
    f = 0; #public double, Double.MAX_VALUE
    g = 0; #public double
    
    # Hardcoded heuristic
    # public double 
    def __init__(self, h):
        global idCounter
        idCounter = idCounter + 1
        self.h = h
        self.id = idCounter
        self.neighbors = []
        self.parent = None
        self.f = 0
        self.g = 0

    def __str__(self):
        return  ("Node " + str(self.id))
    
    def __repr__(self):
        return  ("Node " + str(self.id))
    
    def __lt(self, other):
        return (self.f).__lt__(other.f)
    
    def __gt__(self, other):
        return (self.f).__gt__(other.f)


    def addBranch(self, weight, node):
        newEdge = Edge(weight, node)
        self.neighbors.append(newEdge)
    
    def calculateHeuristic(self, target):
        return self.h

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
                totalWeight = n.g + edge.weight
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

        for i in ids:
            print(str(i), end= ' ')
        print()

n0 = Node(0)
n1 = Node(4)
n2 = Node(3)
n3 = Node(2)
n4 = Node(3)
n5 = Node(2)
n6 = Node(1)
n7 = Node(2)
n8 = Node(1)
n9 = Node(0)

n1.addBranch(0, n2)
n1.addBranch(0, n4)


n2.addBranch(0, n1)
n2.addBranch(0, n3)
n2.addBranch(0, n5)

n3.addBranch(0, n2)
n3.addBranch(0, n6)

n4.addBranch(0, n1)
n4.addBranch(0, n5)
n4.addBranch(0, n7)

n5.addBranch(0, n2)
n5.addBranch(0, n4)
n5.addBranch(0, n8)
n5.addBranch(0, n6)

n6.addBranch(0, n3)
n6.addBranch(0, n5)
n6.addBranch(0, n9)

n7.addBranch(0, n4)
n7.addBranch(0, n8)

n8.addBranch(0, n7)
n8.addBranch(0, n5)
n8.addBranch(0, n9)

n9.addBranch(0, n8)
n9.addBranch(0, n6)

res = Node(0)

res1 = res.aStar(n1, n2)
res2 = res.aStar(n1, n3)
res3 = res.aStar(n1, n4)
res4 = res.aStar(n1, n5)
res5 = res.aStar(n1, n6)
res6 = res.aStar(n1, n7)
res7 = res.aStar(n1, n8)
res8 = res.aStar(n1, n9)

res.printPath(res1)
res.printPath(res2)
res.printPath(res3)
res.printPath(res4)
res.printPath(res5)
res.printPath(res6)
res.printPath(res7)
res.printPath(res8)



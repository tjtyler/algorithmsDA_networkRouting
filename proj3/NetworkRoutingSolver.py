#!/usr/bin/python3


from CS312Graph import *
import time
import math
from abc import ABC, abstractmethod



class NetworkRoutingSolver:
    
    def __init__( self):
        self.dist = []
        self.prev = []

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getEdgeBetweenNodes(self, destIndex):
        #THIS RETURNS THE EDGE BETWEEN destIndex AND ITS previous NODE
        previous = self.prev[destIndex]
        if previous == None:
            return None
        nodes = self.network.getNodes()
        neighbors = nodes[previous].neighbors
        for i in range(0,3):
            if neighbors[i].dest.node_id == destIndex:
                edge = neighbors[i]
                return edge
        return None

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        path_edges = []
        total_length = 0
        #IF THERE IS NO PATH (the dist[destIndex] == Infinity) THEN RETURN INFINITY AND EMPTY path_edges[]
        if self.dist[destIndex] == math.inf:
            return {'cost':self.dist[destIndex], 'path':path_edges}
        #WHEN destIndex == None THAN WE ARE AT THE SOURCE NODE
        while destIndex != None:
            edge = self.getEdgeBetweenNodes(destIndex)
            if edge == None:
                break
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            total_length += edge.length
            destIndex = self.prev[destIndex]
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.dist = []
        self.prev = []
        self.source = srcIndex
        t1 = time.time()
        #node_id's start at 0 and increment by 1
        self.dijkstra(use_heap, self.network, srcIndex)
        t2 = time.time()
        return (t2-t1)

    def dijkstra(self,use_heap,  graph, src):
        if use_heap:
            Q = HeapQueue()
            # Q = Q.makeQueue(graph)
        else:
            Q = ArrayQueue()
            # Q = Q.makeQueue(graph)
        nodes = graph.getNodes()
        for i in range(0,len(nodes)):
            self.dist.append(math.inf)
            self.prev.append(None)
            Q.makeQueue(graph)
        self.dist[src] = 0
        # if use_heap:
        #     Q.decrease_key(src, self.dist)
        while Q.size() > 0:
            u = Q.delete_min(self.dist) # u is the node_id of the min in the Q
            if u == -1:
                break
            u_neighbors = nodes[u].neighbors # a list of u's neighbors (edges)
            for i in range(0,3):
                neighbor_id = u_neighbors[i].dest.node_id #neighbor's node_id
                alt = self.dist[u] + u_neighbors[i].length #alt = the length from u to neighbor[i]
                if alt < self.dist[neighbor_id]:
                    self.dist[neighbor_id] = alt
                    self.prev[neighbor_id] = u
                    # if use_heap:
                    #     Q.decrease_key(neighbor_id, self.dist)
        
        
# INFINITY = 99999999
#-------- ABSTRACT QUEUE CLASS -----------
# class Queue(ABC):
#     @abstractmethod
#     def __init__(self):
#         self.Q = []
#         self.length = 0

#     @abstractmethod
#     def delete_min(self, dist):
#         pass

#     @abstractmethod
#     def decrease_key(self):
#         pass

#     @abstractmethod
#     def insert(self, vertex):
#         pass

#     @abstractmethod
#     def size(self):
#         return self.length

class ArrayQueue:
    def __init__(self):
        self.Q = []
        self.length = 0

    def delete_min(self, dist):
        min_index = None
        min = math.inf
        for i in range(0,len(dist)):
            if (dist[i] < min) and (self.Q[i] != None):
                min = dist[i]
                min_index = i
        if min != math.inf:
            self.Q[min_index] = None
            self.length -= 1
            return min_index
        return -1

    def makeQueue(self, graph):
        nodes = graph.getNodes()
        for i in range(0,len(nodes)):
            self.insert(nodes[i].node_id)
        return self.Q

    def decrease_key(self):
        pass

    def insert(self, vertex):
        self.Q.append(vertex)
        self.length += 1

    def size(self):
        return self.length



class HeapQueue:
    def __init__(self):
        self.Q = []
        self.PointerArr = []
        self.length = 0

    def delete_min(self, dist):
        if self.length == 0:
            return None
        else:
            min_index = self.Q[0]
            self.sift_down(self.Q[self.length],1,dist)
            return min_index

    def decrease_key(self, node_id, dist):
        self.bubble_up(node_id, self.PointerArr[self.length], dist)

    def insert(self, vertex, dist):
        self.bubble_up(vertex, self.length + 1, dist)

    def bubble_up(self,node_id, lastIndex, dist):
        i = lastIndex
        p = math.ceil(i/2)
        while (i != 0) and (dist[p] > dist[i]):
            self.Q[i] = self.Q[p]
            i = p
            p = math.ceil(i/2)
        self.Q[i] = node_id

    def sift_down(self, node_id, i, dist):
        c = self.minchild(i, dist)
        while (c != 0) and (dist[c] < dist[node_id]):
            self.Q[i] = self.Q[c]
            i = c
            c = self.minchild(i,dist)
        self.Q[i] = node_id
    
    def minchild(self, i, dist):
        #RETURN THE INDEX OF THE SAMLLEST CHILD OF h(i)
        if 2*i > self.length:
            return 0 # no children
        else:
            left_child = dist[2*i+1]

            if (2*i+2) <= self.length:
                right_child = dist[2*i+2]
                if right_child < left_child:
                    return right_child
            return left_child

    def size(self):
        return self.length

    def makeQueue(self, graph):
        nodes = graph.getNodes()
        self.Q = [None] * len(nodes)
        for i in range(0,len(nodes)):
            self.Q[i] = graph.getNodes()[i]


    #leftchild = (2*i) + 1
    #rightchild = (2*i) + 2

    #deletemin():
        #swap (first, last)
        
#---------END MYCLASSES-------------------
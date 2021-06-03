import heapq  
import time
global graph_ver3
graph_ver3 = {}
global path_dict 
path_dict= {}
global idCounter
idCounter = 0

class Node():
    def __init__(self, latitude, longitude):
        global idCounter
        idCounter = idCounter + 1
        self.h = 0
        self.id = str(idCounter)
        self.latitude = latitude
        self.longitude = longitude
        path_dict[self.id] = []
      
    def __str__(self):
      return self.id
    
    def addBranch(self, weight, traffic, node):
        if self.id in graph_ver3.keys():
            addition = graph_ver3[self.id]
            addition[str(node)] = [weight, traffic]
            graph_ver3[self.id] = addition
        else: 
            graph_ver3[self.id] = {str(node) : [weight, traffic]}

    def changeBranch(self, traffic, node) :
      try:
        modify_node = graph_ver3[self.id]
        modify_node[node.id][1] = traffic
        graph_ver3[self.id] = modify_node
      except Exception as e:
        print(e)
        print('Change node error %s -> %s' %(self.id, node))

    def dijkstra(self, graph, path_dict, start, end):
      distances = {node: float('inf') for node in graph}  
      distances[start] = 0  
      queue = []
      heapq.heappush(queue, [distances[start], start])

      while queue: 
        current_distance, current_destination = heapq.heappop(queue)  

        if distances[current_destination] < current_distance: 
          continue
        
        for new_destination, new_distance in graph[current_destination].items():
          distance = current_distance + new_distance[0]/new_distance[1] 
          if distance < distances[new_destination]:  
            distances[new_destination] = distance
            path_dict[new_destination] = path_dict[current_destination] + [current_destination]
            heapq.heappush(queue, [distance, new_destination]) 
        
      return path_dict[end]

start = time.time()
result = n0.dijkstra(graph_ver3, path_dict, '65', '39') #graph, path, start node, end node
print(result)
print("Dijstra time: "+ str(time.time()-start))

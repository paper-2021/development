import heapq  

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
    
    def addBranch(self, weight, node):
        if self.id in graph_ver3.keys():
            addition = graph_ver3[self.id]
            addition[str(node)] = weight
            graph_ver3[self.id] = addition
        else: 
            graph_ver3[self.id] = {str(node) : weight}
    
    def __str__(self):
        return self.id
    

def dijkstra(graph, start, path_dict):
  distances = {node: float('inf') for node in graph}  
  distances[start] = 0  
  queue = []
  heapq.heappush(queue, [distances[start], start])

  while queue:  # queue에 남아 있는 노드가 없으면 끝
    current_distance, current_destination = heapq.heappop(queue)  

    if distances[current_destination] < current_distance: 
      continue
    
    for new_destination, new_distance in graph[current_destination].items():
      distance = current_distance + new_distance  
      if distance < distances[new_destination]:  
        distances[new_destination] = distance
        path_dict[new_destination] = path_dict[current_destination] + [current_destination]
        heapq.heappush(queue, [distance, new_destination]) 
    
  return distances, path_dict


# 이부분에 하면 Aster의 Node와 addBranch 길찾기 실행 가능

dijkstra(graph_ver3, '21', path_dict)
print(path_dict['3'])


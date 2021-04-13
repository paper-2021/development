import heapq  

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

path_dict1 = {'1' : [], '2' : [], '3' : [], '4' : [], '5' : [], '6' : [], '7' : [], '8' : [], '9' : []}
path_dict2 = {'1' : [], '2' : [], '3' : [], '4' : [], '5' : [], '6' : [], '7' : [], '8' : [], '9' : []}

graph1 = { # current map
    '1': {'2': 0, '4': 0},
    '2': {'1' : 0, '5' : 0, '3' : 0},
    '3': {'2' : 0, '6' : 0},
    '4': {'1' : 0, '5' : 0, '7' : 0},
    '5': {'2': 0, '4' : 0, '8' : 0, '6' : 0},
    '6': {'3' : 0, '5' : 0, '9' : 0},
    '7': {'4' : 0, '8' : 0},
    '8': {'7' : 0, '5' : 0, '9' : 0},
    '9': {'8' : 0, '6' : 0},
}
graph2 = { # current map
    '1': {'2': 10, '4': 10},
    '2': {'1' : 5, '5' : 5, '3' : 0},
    '3': {'2' : 0, '6' : 5},
    '4': {'1' : 5, '5' : 0, '7' : 10},
    '5': {'2': 0, '4' : 0, '8' : 0, '6' : 5},
    '6': {'3' : 5, '5' : 0, '9' : 5},
    '7': {'4' : 10, '8' : 0},
    '8': {'7' : 5, '5' : 5, '9' : 0},
    '9': {'8' : 5, '6' : 0},
}

print(dijkstra(graph1, '1', path_dict1))
print(dijkstra(graph2, '1', path_dict2))
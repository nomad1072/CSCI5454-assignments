# Github Repo - https://github.com/nomad1072/CSCI5454-assignments

from collections import defaultdict
import pickle
import os
import random

class Graph:

    def __init__(self):
        self.adjacencyList = defaultdict(list)

    def insert(self, u, v):
        self.adjacencyList[u].append(v)
    
    def largest_degree(self):
        largest_vertex, length = -1, 0
        for key, value in self.adjacencyList.items():
            print('Key: ', key)
            print('Value: ', value)
            number_of_edges = len(value)
            if number_of_edges > length:
                length = number_of_edges
                largest_vertex = key
        
        return largest_vertex, length

    def average_degree(self):
        number_of_edges, vertices_count = 0, 0
        for key, value in self.adjacencyList.items():
            print('Key: ', key)
            print('Value: ', value)
            vertices_count += 1
            number_of_edges += len(value)
        
        if vertices_count == 0:
            return -1
        else:
            return number_of_edges / vertices_count

    def prune(self, returned_vertices, visited_vertices):
        for vertex in returned_vertices:
            if vertex not in visited_vertices:
                visited_vertices.append(vertex)

        return visited_vertices


    def calculateDorLess(self, v, depth, current_vertices, visited_vertices=[]):
        if depth == 0:
            return current_vertices
        # print('Adjacent Vertices of ', v, " are: ", self.adjacencyList[v])
        for u in self.adjacencyList[v]:
            current_vertices = []
            if u not in visited_vertices:
                visited_vertices.append(u)
                current_vertices.append(u)
                returned_vertices = self.calculateDorLess(u, depth - 1, current_vertices, visited_vertices)
                # print('**************************************************************************************************')
                # print('U: ', u)
                # print('Returned Vertices: ', returned_vertices)
                # print('**************************************************************************************************')
                visited_vertices = self.prune(returned_vertices, visited_vertices)

        return (visited_vertices)

    def alternateSolution(self, v, depth, visited_vertices=[]):
        queue = list()
        queue.append((v, depth))
        while len(queue) != 0:
            vertex, depth = queue.pop(0)
            if depth < 0:
                return visited_vertices

            visited_vertices.append(vertex)
            adjacentVertices = self.adjacencyList[v]
            for vertex in adjacentVertices:
                queue.append((vertex, depth-1))

            print('Queue: ', queue)
            print('Visited Vertices: ', visited_vertices)

        return visited_vertices


if os.path.exists('./Results.pickle'):
    f = open("Results.pickle", "rb")
    new_graph = pickle.load(f)
    metrics = pickle.load(f)
    print('Metrics: ', metrics)

    # print('Results: ', new_graph.calculateDorLess("0", 500, []))
    l = [random.randint(0,1000) for i in range(10)]
    for number in l:
        print('**************************************************************************************************')
        print('Results for vertex: ', number )
        print('Results: ', len(new_graph.calculateDorLess(str(number), 50, [])))
        print('**************************************************************************************************')

    f.close()
else:
    with open('./roadNet-TX.txt') as fp:
        line = fp.readline()
        new_graph = Graph()
        cnt = 1
        while line:
            if cnt >= 5:
                numbers = line.strip().split("\t")
                print('Numbers: ', numbers)
                new_graph.insert(numbers[0], numbers[1])
            line = fp.readline()
            cnt += 1

        largest_vertex, length = new_graph.largest_degree()
        average_degree = new_graph.average_degree()

        f = open('Results.pickle', "wb")

        pickle.dump(new_graph, f)
        pickle.dump({ "largest_vertex": largest_vertex, "number_of_edges": length, "average_degree": average_degree }, f)

        f.close()
        print('Largest Vertex: ', largest_vertex, " number of edges: ", length)
        print('Average Degree: ', average_degree)
        print('Elements at less than 2: ', new_graph.calculateDorLess(largest_vertex, 2, [largest_vertex]))


print('Program end!')
    
    


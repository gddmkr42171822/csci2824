# 
# CSCI 2824 Application 2
# 
# I created my own data set with the letters off the alphabet and gave each edge an arbitrary number
# I used a python libarary called NetworkX to create the graph to be traversed.
# I chose to do the nearest neighbor, repeated nearest neighbor, and exhaustive search algorithms.
# I collaborated with Nick Smith and Nathan Gilles in order to complete this assignment.
#
# RESULTS:
#   Nearest Neighbor had a time of .0003719 seconds.
# 	Repeated Nearest Neighbor had a time of .0025460 seconds.
#	Exhaustive Search had a time of 93.2886030 seconds. 
# Each of the searches had different solutions but it seemed that the exhaustive search came out with the shortest path
# that had the lowest sum of weights of all of the edges.  Nearest neighbor came back with the longest path depending on 
# which node it started with while nearest neighbor came back with the second shortest path next to exhaustive search.
# Exhaustive search took much longer than the rest of the searches.  Nearest Neighbor was of course faster than repeated
# nearest neighbor.





import networkx as nx
import csv
import matplotlib.pyplot as plt
import random
import itertools
import time
# coding: utf-8

# Build a graph from the csv data in cities.csv file
G=nx.Graph()
with open('cities.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for row in reader:
        G.add_edge(row[2], row[0], {'weight':row[1]})
        

#
#
#
#nearest neighbor
#
#
#

def get_neighbor_nodes(node, Graph):
	smallest_weight = {}
	for each in G[node]:
		smallest_weight[(G[node][each]['weight'])] = each
	return smallest_weight
			
def my_key(dict_key):
     try:
         return int(dict_key)
     except ValueError:
         return dict_key
			
def get_smallest_weight(dictionary_of_neighbors):
	sorted_dictionary_of_neighbors = sorted(dictionary_of_neighbors, key=my_key)
	min_key = sorted_dictionary_of_neighbors[0]
	neighbor_with_smallest_weight = dictionary_of_neighbors[min_key]
	return neighbor_with_smallest_weight
	
def remove_visited_nodes(dictionary_of_neighbors, path):
	for key,value in dictionary_of_neighbors.items():
		if value in path:
			del dictionary_of_neighbors[key]
	return dictionary_of_neighbors
		
	
def find_start_node(node, start_node):
	weight_to_start = G[node][start_node]
	return (start_node, weight_to_start)
	
	
start_time2 = time.time()

def nearest_neighbor(node, path, num_nodes):
	num_nodes += 1
	path.append(node)
	if num_nodes == G.number_of_nodes():
		start_node, weight_to_start = find_start_node(node, path[0])
		path.append(start_node)
	neighbor_nodes = get_neighbor_nodes(node, G)
	checked_for_visited = remove_visited_nodes(neighbor_nodes, path)
	isempty = (checked_for_visited and True) or False
	if not isempty:
		return path
	neighbor_with_smallest_weight = get_smallest_weight(checked_for_visited)
	nearest_neighbor(neighbor_with_smallest_weight, path, num_nodes)
	return path
		
random_node = random.choice(G.nodes())
num_nodes = 0
path = []
print nearest_neighbor('a', path, num_nodes)

print "Nearest Neighbor starting with a"
print time.time() - start_time2, "seconds"

#
#
#
#repeated nearest neighbor
#
#
#

start_time1 = time.time()

def get_smallest_weight_and_cost(curr_node, dictionary_of_neighbors, cost):
	sorted_dictionary_of_neighbors = sorted(dictionary_of_neighbors, key=my_key)
	min_key = sorted_dictionary_of_neighbors[0]
	neighbor_with_smallest_weight = dictionary_of_neighbors[min_key]
	
	cost += float(min_key)
	return (neighbor_with_smallest_weight, min_key)
	


def repeated_nearest_neighbor(node, repeated_path, cost, num_nodes):
	repeated_path.append(node)
	num_nodes += 1
	if num_nodes == G.number_of_nodes():
		start_node, weight_to_start = find_start_node(node, repeated_path[0])
		repeated_path.append(start_node)
		cost += float(weight_to_start['weight'])
		return (repeated_path,cost)
	neighbor_nodes = get_neighbor_nodes(node,repeated_path)
	checked_for_visited = remove_visited_nodes(neighbor_nodes, repeated_path)
	isempty = (checked_for_visited and True) or False
	if not isempty:		
		return	(repeated_path,cost)
	neighbor_with_smallest_weight, add_cost = get_smallest_weight_and_cost(node,checked_for_visited, cost)
	cost += float(add_cost)
	dummy_node, path_cost = repeated_nearest_neighbor(neighbor_with_smallest_weight, repeated_path, cost, num_nodes)
	return (repeated_path,path_cost)

#run nearest neighbor over all the nodes in the graph turning it into repeated nearest neighbor
befcost = 10000
dict_of_paths = {}
for each in G.nodes():
	cost = 0.00
	repeated_path = []
	repeated_num_nodes = 0
	path, cost = repeated_nearest_neighbor(each, repeated_path, cost, repeated_num_nodes)
	if cost <= befcost:
		dict_of_paths.clear()
		dict_of_paths[each] = [(path,cost)]
		befcost = cost
print dict_of_paths.values()
print "Repeated Neighbor Time"
print time.time() - start_time1, "seconds"



#exhaustive search

start_time = time.time()

def get_distance_between_2nodes(node_one, node_two):
	return G[node_one][node_two]['weight']
	
listperm = itertools.permutations(['a','b', 'c','d', 'e', 'f', 'g', 'h', 'i', 'j'])
last_value = 0
first_value = 0
offset = 0
total = []
#total.append(0.0)
for y in listperm:
	total.append(0.0)
#print total
k = -1
j = 0

# make a list of permutations of all the nodes for exhaustive search
listperm = itertools.permutations(['a','b', 'c','d', 'e', 'f', 'g', 'h', 'i', 'j'])
path_of_perms = []

for x in listperm:
    path_of_perms.append(x)
    offset = 0
    for i in x:
    	offset += 1
    	if offset > 1 and i != last_value:
    		total[j] += float(get_distance_between_2nodes(last_value,i))
    		if offset >= len(x):
    			total[j] += float(get_distance_between_2nodes(first_value, i))
    	elif offset == 1:
    		first_value = i
    	last_value = i
    j += 1
    
# associate each path with their respective sum of weights
d = dict(zip(total,path_of_perms))
new_d = sorted(d, key=my_key)

print d[new_d[0]]
print new_d[0]


print "Exhaustive Search"
print time.time() - start_time, "seconds"

# cities.csv data
"""
a,78,b
a,95,c
a,3,d
a,40,e
a,5,f
a,49,g
a,7,h
a,200,i
a,9,j
b,10,c
b,90,d
b,12,e
b,105,f
b,14,g
b,15,h
b,305,i
b,17,j
c,18,d
c,35,e
c,76,f
c,59,g
c,22,h
c,23,i
c,24,j
d,25,e
d,260,f
d,27,g
d,28,h
d,29,i
d,0.5,j
e,31,f
e,32,g
e,33,h
e,67,i
e,35,j
f,36,g
f,37,h
f,12,i
f,39,j
g,67,h
g,41,i
g,69,j
h,43,i
h,44,j
i,81,j
"""



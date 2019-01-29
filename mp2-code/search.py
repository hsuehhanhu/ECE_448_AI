# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
import sys
import queue as queue
from itertools import permutations
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod, [])(maze)

def bfs(maze):
    # TODO: Write your code here    
    return [], 0

def dfs(maze):
    # TODO: Write your code here    
    return [], 0

def greedy(maze):
    # TODO: Write your code here    
    return [], 0

def astar(maze):
    # TODO: Write your code here 
    
    cur_pos = maze.getStart()
    dimensions = maze.getDimensions()
    visited = [[False for x in range(dimensions[1])] for y in range(dimensions[0])]
    pellet_arr = [[0 for x in range(dimensions[1])] for y in range(dimensions[0])]
    came_from = [[() for x in range(dimensions[1])] for y in range(dimensions[0])]
    num_states_explored = 0;
    frontier = queue.PriorityQueue()
    distance = heuristic(maze,cur_pos)
    frontier.put([distance,cur_pos])
    came_from[cur_pos[0]][cur_pos[1]] = None
    cost_so_far = {}
    cost_so_far[cur_pos] = 0
    prev = cur_pos
    prev_goal = cur_pos
    optimal = []
    prim_list = maze.getObjectives()
    prim_list.insert(0,cur_pos)
    obj_list = maze.getObjectives()
    pellets = 0
    cur_goal = closest_goal(cur_pos,obj_list)
    mst_sum = 0

    

    while not frontier.empty():
        cur_pos = frontier.get()
        location = cur_pos[1] #set location to the coordinates
    
        neighbors = maze.getNeighbors(location[0],location[1])

        if(location in obj_list):
            obj_list.remove(location) #if location is an objective then we move it from the objective list
            frontier.queue.clear() #clear the priority queue since we will move on to another objective
            if(obj_list):
                cur_goal = closest_goal(location,obj_list) #if obj_list is not empty, we set the current goal to the closest goal
                del prim_list[0] #remove the first item from prim list
                prim_list.remove(location) #remove the objective we found
                prim_list.insert(0,location) #add the objective we found to the start
                #mst_sum = prim(location,prim_list) #calculate the sum of minimum spanning tree

            prev = location
            pellets +=1 #increment pellets if we reached a goal
            while prev != prev_goal:
                prev = came_from[prev[0]][prev[1]] #while prev is not equal to the previous goal, then we set prev to what it came from
                optimal.append((prev[0],prev[1])) #append prev to the optimal path
            prev_goal = location 

            if(pellets == 1):
                optimal.append((location[0],location[1])) #if pellets equals the # of objectives, we append the location to the optimal path
                return(optimal,num_states_explored)

        if(visited[location[0]][location[1]] == False):
            visited[location[0]][location[1]] = True #if we have not visited if before, set it to visited
            num_states_explored += 1

        for i in neighbors:
            if (i[0] > dimensions[0] or i[1] > dimensions[1]):
                continue

            new_cost = cost_so_far[location] + 1 #add 1 since each move is 1 unit cost
            if i not in cost_so_far or new_cost < cost_so_far[i]: #if it's not an old location or if the new cost is lower than the cost so far
                cost_so_far[i] = new_cost
                distance = new_cost + manhattan(i,cur_goal) + mst_sum 
                frontier.put([distance,i]) #put the neighbor and its distance into the priority queue
                came_from[i[0]][i[1]] = location

            if pellet_arr[i[0]][i[1]] < pellets: # used to check the current state and the state at the i location
                pellet_arr[i[0]][i[1]] = pellets
                cost_so_far[i] = new_cost
                distance = new_cost + manhattan(i,cur_goal) + mst_sum
                frontier.put([distance,i])
                came_from[i[0]][i[1]] = location

    return [], 0

'''
heuristic used for greedy. calculates the manhattan distance from the cur pos to the goal
'''
def heuristic(maze, cur_pos):
    objectives = maze.getObjectives()
    goal = objectives[-1]
    return abs(goal[0] - cur_pos[0]) + abs(goal[1] - cur_pos[1])
'''
is used in a* to calculate the manhattan distance betwee two points
'''
def manhattan(cur_pos,goal):
    return abs(goal[0] - cur_pos[0]) + abs(goal[1] - cur_pos[1])
'''
prim is used to generate the mst for the objectives and return the edge cost of the tree
'''  
def prim(cur_pos,obj_list):
    edges = []
    edge = ()
    distance = 0
    mst = []
    smalledge = queue.PriorityQueue()
    edge_sum = 0

    # will generate all the edges for the objectives
    for x in range (0,len(obj_list)-1):
        for y in range(x+1,len(obj_list)):
            distance = manhattan(obj_list[x],obj_list[y])
            edge  = (distance,obj_list[x],obj_list[y])
            edges.append(edge)

    #will push the edges from our starting position to the queue first
    for e in edges:
        if e[1] == cur_pos:
            smalledge.put(e)

    # will run until all the objectives are connected
    while(len(mst) != len(obj_list)-1):
        min_edge = smalledge.get() # min edge also has the distance within it
        
        # print(edges)
        if min_edge in edges:
            mst.append(min_edge)
            edges.remove(min_edge)
        
        for e in edges:
            if e[1] == min_edge[2]:
                smalledge.put(e)
    for i in mst:
        edge_sum += i[0]

    return edge_sum
        
'''
Calculates the closest goal to a given position and returns that goal
'''
def closest_goal(cur_pos,obj_list):
    que = queue.PriorityQueue()
    for i in obj_list:
        distance = manhattan(cur_pos,i)
        que.put((distance,i))
    goal = que.get()
    return goal[1]
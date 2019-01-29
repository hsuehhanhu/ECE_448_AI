# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
import numpy as np
from const import *

def computeCoordinate(start, length, angle):
    """Compute the end cooridinate based on the given start position, length and angle.

        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to counter-clockwise

        Return:
            End position of the arm link, (x-coordinate, y-coordinate)
    """
    radians = angle*(math.pi/180)   #switch the angle to radians  
    x = length*math.cos(radians)    #find the horizontal length
    y = length*math.sin(radians)    #find the vertical length

    end_pos = (start[0]+x,start[1]-y) #add the hor. length to the x and the vert. length to the y to find the end_pos
    return end_pos
    pass

def doesArmTouchObstacles(armPos, obstacles):
    """Determine whether the given arm links touch obstacles

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            obstacles (list): x-, y- coordinate and radius of obstacles [(x, y, r)]

        Return:
            True if touched. False it not.
    """    
    
    check = False

    for link in armPos:
        #store the start and end points of each link
        linkStart = link[0]
        linkEnd = link[1]
        x1 = linkStart[0]
        y1 = linkStart[1]
        x2 = linkEnd[0]
        y2 = linkEnd[1]
        if x1 == x2:
            m = float("inf") #if the x coordinates of the start of the link and the end of the link then we set a lower bound
        else:
            m = (y2 - y1) / (x2 - x1)   #y = mx + b # starts off at a division of zero since both start and end are at the same x location

        b = y1 - m * x1 # the y intercept

        linkDistance = math.sqrt((y2-y1)**2 + (x2-x1)**2)
        for circle in obstacles:
            # Calculate the parameters needed for the quadratic formula
            A = (m ** 2 + 1) 
            B = 2*( m * b - m * circle[1] - circle[0])
            C = (circle[1]**2 - circle[2]**2 + circle[0]**2 - 2*(b * circle[1]) + b**2)

            x = quadratic(A,B,C)

            if(x[0] != -1): #if the quadratic returns a positive value then theres an intersection point
                if(x[1] == -1): #theres only one intersection point needed to be checked
                    x.remove(x[1])
                    y = [m*x[0]+b]
                else:
                    y = [m*x[0]+b,m*x[1]+b]

                #will check if the intersection is happening by the link or just the line the link represents
                for i in range(0,len(x)):
                    linkDistance = math.sqrt((y2-y1)**2 + (x2-x1)**2)
                    pointToStart = math.sqrt((y[i]-y1)**2 + (x[i]-x1)**2)
                    pointToEnd = math.sqrt((y[i]-y2)**2 + (x[i]-x2)**2)

                    #if the distances match then the link is touching an obstacle
                    if(linkDistance - 0.5 <=(pointToEnd + pointToStart) <= linkDistance+0.5):
                        return True
                    
                
            
                
    return check

        


def doesArmTouchGoals(armEnd, goals):
    """Determine whether the given arm links touch goals

        Args:
            armEnd (tuple): the arm tick position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]

        Return:
            True if touched. False it not.
    """
    for circle in goals:
        x_incircle = math.pow((armEnd[0] - circle[0]),2)
        y_incircle = math.pow((armEnd[1] - circle[1]),2) 
        in_circle = x_incircle + y_incircle #find the euclidean distance from the end of the arm to the center of the circle.
        if(in_circle <= math.pow(circle[2],2)): #if the euc. distance is less than or equal to the range of the circle then we are touch the goal
            return True
    return False


def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False it not.
    """
    check = True

    for arm in armPos:
        linkStart = arm[0]
        linkEnd = arm[1]
        x1 = linkStart[0]
        y1 = linkStart[1]
        x2 = linkEnd[0]
        y2 = linkEnd[1]
        #print("x:{} y:{}".format(x1,y1))
        
       
        if((0<=x1<=window[0]) and (0<=x2<=window[0]) and (0<=y1<=window[1]) and (0<=y2<window[1])): #if the coordinates of the start of the link and the end of the link are within bounds then return true
            check = True
        else:
            
            return False

    return check

def quadratic(A,B,C):
    
    D = (B**2)-(4*A*C) # discriminant
    x1 = -1
    x2 = -1
    if D < 0:
        return ([x1,x2]) #if discriminant is -1 we have nothing
    elif D == 0:
        x1 = (-B+math.sqrt(D))/(2*A) #if disc. is 0 then we have one point
        return([x1,x2])
    else:
        x1 = (-B+math.sqrt(D))/(2*A) #if disc is positive, then we have two points
        x2 = (-B-math.sqrt(D))/(2*A)
        return ([x1,x2])
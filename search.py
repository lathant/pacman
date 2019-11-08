# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"


    stacknode = util.Stack()                    #this stack will house all nodes that are being considered
    stackpath = util.Stack()                    #this stack will house the path associated with each node
                                                #these will be popped and pushed simutaniously to maintain sync


    visitednode = []                            #this array holds all nodes that are visited by that search


    stacknode.push(problem.getStartState())     #insert the startpoint into node stack
    stackpath.push([])                          #insert startpath (no directions taken) into path stack


    while not stacknode.isEmpty():              #if the stack is empty then all nodes have been looked at
        currentnode = stacknode.pop()
        currentpath = stackpath.pop()

        if  problem.isGoalState(currentnode):   #check if goal was reached
            return currentpath

        if currentnode not in visitednode:
            visitednode.append(currentnode)     #mark a node as visited
            neighbours = problem.getSuccessors(currentnode)     #retrieve all nodes that can be reached from current node


            for item in neighbours:
                potentialpath = currentpath + [item[1]]         #current path is updated with step to neighbour node
                stacknode.push(item[0])                         #node and path are pushed onto respective stacks
                stackpath.push(potentialpath)



    print("error no solution found")                            #error messaged should no path be found
    return []
    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    nodequeue = util.Queue()                    #this queue will hold all the nodes that we will be looking at
    pathqueue = util.Queue()                    #this queue will hold the path to the nodes that will be stored in nodequeue

    visitednode = []

    nodequeue.push(problem.getStartState())     #push the start node and empty array as path into respective queues
    pathqueue.push([])

    while not nodequeue.isEmpty():
        currentnode = nodequeue.pop()           #pop the node and pathqueue into local variables
        currentpath = pathqueue.pop()

        if problem.isGoalState(currentnode):    #Check if the goal has been reached
            return currentpath

        if currentnode not in visitednode:      #if node is not visited
            visitednode.append(currentnode)     #add node to list of visited node

            neighbours = problem.getSuccessors(currentnode)         #get the adjacent nodes

            for item in neighbours:
                updatedpath = currentpath + [item[1]]
                nodequeue.push(item[0])                             #for each new push the path to the node into nodequeue
                pathqueue.push(updatedpath)                         #also push the node into the nodequeue
                                                                    #nodes are pushed and popped at the same time to maintain sync

    print("error no paths found")
    return[]
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    statePriorityQueue = util.PriorityQueue()          #creates a priority queue for graph search
    state = (problem.getStartState(),[], 0)            #tuple containing the start location, empty path array and 0 as cost to reach node
    statePriorityQueue.push(state,0)                   #place state and priority into the queue
    visitednodes = []

    while not statePriorityQueue.isEmpty():
        currentstate = statePriorityQueue.pop()         #dequeue the lowest priority node off the queue

        statenode = currentstate[0]                     #retrieve the node from the queue item
        statepath = currentstate[1]                     #retrieve the path to the the node
        statepriority = currentstate[2]                 #retrieve the priority cost of reaching node

        if problem.isGoalState(statenode):
            return statepath

        if statenode not in visitednodes:
            visitednodes.append(statenode)              #add node to visited list
            neighbours = problem.getSuccessors(statenode)   #retrieve adjacent nodes

            for item in neighbours:
                updatedpriority = item[2] + statepriority       #calculate cost of reaching the adjacent node
                newnode = item[0]                               #retrieve the node address
                updatedpath = statepath + [item[1]]             #update the path to this node

                newstate = (newnode,updatedpath,updatedpriority)    #create a tuple containing all the information
                statePriorityQueue.push(newstate, updatedpriority)  #enqueue the node with the cost

    print("error no path found")
    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    startHeuristic = heuristic(problem.getStartState(),problem)
    statePriorityQueue = util.PriorityQueue()               #creates a priority queue for graph search
    state = (problem.getStartState(),[], startHeuristic, 0) #tuple containing the start location, empty path array and the current heuristic value and 0 as the starting cost of path
    statePriorityQueue.push(state,startHeuristic)           #place state and priority into the queue
    visitednodes = []

    while not statePriorityQueue.isEmpty():
        currentstate = statePriorityQueue.pop()             #dequeue the lowest priority node off the queue

        statenode = currentstate[0]                         #retrieve the node from the queue item
        statepath = currentstate[1]                         #retrieve the path to the the node
        stateHeuristic = currentstate[2]                    #retrieve the heuristic for the current node
        stateCost = currentstate[3]                         #retrieve the cost of the path for the current state

        if problem.isGoalState(statenode):
            return statepath

        if statenode not in visitednodes:                   #if node hasn't been visited, add to visited node list
            visitednodes.append(statenode)
            neighbours = problem.getSuccessors(statenode)   #get the successors of the current node

            for item in neighbours:
                updatedCost = stateCost + item[2]           #update the cost of the path
                newnode = item[0]
                updatedPath = statepath + [item[1]]
                newHeuristic = heuristic(newnode,problem)   #retrieve the heuristic for the node
                newpriority = newHeuristic + updatedCost    #set the priority as the sum of cost and heurisitc
                newstate = (newnode,updatedPath,newHeuristic,updatedCost)
                statePriorityQueue.push(newstate,newpriority)   #push into the priority queue

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

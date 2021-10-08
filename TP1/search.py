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
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
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
    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 1 ICI
    '''
    visitedStates = set()
    solution = []
    stack= util.Stack()
    initialPosition = problem.getStartState()
    stack.push({'position':initialPosition, 'path':[]})
    continu = True
    while continu:
        if stack.isEmpty():
            continu = False
        else:
            element = stack.pop()
            if problem.isGoalState(element['position']):
                solution = element['path']
                continu = False
            else:
                if element['position'] not in visitedStates:
                    visitedStates.add(element['position'])
                    successors = problem.getSuccessors(element['position'])
                    for s in successors:
                        path = element['path'].copy()
                        path.append(s[1])
                        stack.push({'position':s[0], 'path':path})

        #cheker si stack est vide, si oui on quitte, sinon...
        #prend premier de stack (pop)
        # check si c'est le goal
        # si oui on quitte, sinon
        # on met lelement dans visité
        # on prend ses successeurs,
        # on y associe le chemin de son parent
        # et pn les mets dans le stack
    return solution


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""


    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 2 ICI
    '''
    visitedStates = []
    solution = []
    queue= util.Queue()
    initialPosition = problem.getStartState()
    queue.push({'position':initialPosition, 'path':[]})
    continu = True
    while continu:
        if queue.isEmpty():
            continu = False
        else:
            element = queue.pop()
            if problem.isGoalState(element['position']):
                print("visitedStates")
                for i in visitedStates:
                    print(i)
                solution = element['path']
                continu = False
            else:
                #est ce que cet element a ete visite
                #print('element[position] ', element['position'])
                #print(visitedStates)
                if element['position'] not in visitedStates:
                    visitedStates.append(element['position'])
                    successors = problem.getSuccessors(element['position'])
                    for s in successors:
                        path = element['path'].copy()
                        path.append(s[1])
                        queue.push({'position':s[0], 'path':path})
    #print(solution)
    return solution


def uniformCostSearch(problem):
    """Search the node of least total cost first."""


    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 3 ICI
    '''
    visitedStates = set()
    solution = []
    queue = util.PriorityQueue()
    initialPosition = problem.getStartState()
    queue.push({'position': initialPosition, 'path': [], 'priority': 0}, 0)
    continu = True
    while continu:
        if queue.isEmpty():
            continu = False
        else:
            element = queue.pop()
            if problem.isGoalState(element['position']):
                solution = element['path']
                continu = False
            else:
                # est ce que cet element a ete visite
                if element['position'] not in visitedStates:

                    visitedStates.add(element['position'])
                    successors = problem.getSuccessors(element['position'])
                    for s in successors:
                        path = element['path'].copy()
                        path.append(s[1])
                        cumulativePriority = s[2] + element['priority']
                        queue.push({'position': s[0], 'path': path, 'priority': cumulativePriority }, cumulativePriority )
    return solution

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 4 ICI
    '''

    visitedStates = []
    solution = []
    queue = util.PriorityQueue()
    initialPosition = problem.getStartState()
    priority = 0
    queue.push({'position': initialPosition, 'path': [], 'priority': priority},
               priority + heuristic(initialPosition, problem))
    continu = True
    while continu:
        if queue.isEmpty():
            continu = False
        else:
            element = queue.pop()
            if problem.isGoalState(element['position']):
                solution = element['path']
                continu = False
            else:
                # est ce que cet element a ete visite
                #print("element['position']" , element['position'])
                #print("visitedStates",visitedStates)
                if element['position'] not in visitedStates:

                    visitedStates.append(element['position'])
                    successors = problem.getSuccessors(element['position'])
                    for s in successors:
                        path = element['path'].copy()
                        path.append(s[1])
                        cumulativePriority = s[2] + element['priority']
                        queue.push({'position': s[0], 'path': path, 'priority': cumulativePriority},
                                   cumulativePriority+heuristic(s[0], problem))
    return solution


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

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
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()

    explored = []

    # act = []

    strt_state = problem.getStartState()
    strt_node = (strt_state, [])

    frontier.push(strt_node)

    # print("Start:", strt_state)
    # print("Node:", strt_node)
    # print("Start's successors:", problem.getSuccessors(strt_state))

    # print("Frontier:", frontier)
    # import time
    while frontier:
        state, act = frontier.pop()
        # print(f'state: {state}, act: {act}')
        # print(f'explored: {explored}')
        if state not in explored:
            explored.append(state)

            if problem.isGoalState(state):
                return act
            
            else:
                succ = problem.getSuccessors(state)
                # print(f'successors: {succ}')
                for s, a, c in succ:
                    path = act + [a]
                    node = (s, path)
                    frontier.push(node)

        # return act

    # time.sleep(2)

    # return act

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    front = util.Queue()

    expl = []

    strt_state = problem.getStartState()
    strt_node = (strt_state, [])

    front.push(strt_node)

    while front:
        state, act = front.pop()

        if state not in expl:
            expl.append(state)

            if problem.isGoalState(state):
                print(act)
                return act
            else:
                for s, a, c in problem.getSuccessors(state):
                    path = act+[a]
                    node = (s, path)
                    front.push(node)

    # util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    front = util.PriorityQueue()
    expl = {}

    strt_state = problem.getStartState()
    strt_node = (strt_state, None, None, 0) # state, parent, action, cost

    front.push(strt_node, 0)

    while front:
        state, p, act, cost = front.pop()

        if state not in expl or cost < expl[state][2]:
            expl[state] = [p, act, cost]

            if problem.isGoalState(state):
                path = []
                while expl[state][0] != None:
                    path.append(expl[state][1])
                    state = expl[state][0]

                return path[::-1]

            else:
                for s, a, c in problem.getSuccessors(state):
                    new_cost = c + cost
                    node = (s, state, a, c)

                    front.update(node, new_cost)

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
    front = util.PriorityQueue()
    expl = {}

    strt_state = problem.getStartState()
    strt_node = (strt_state, None, None, 0) # state, parent, action, cost

    front.push(strt_node, 0)

    while front:
        state, p, act, cost = front.pop()

        expl[state] = [p, act, cost]

        if problem.isGoalState(state):
            path = []
            while expl[state][0] != None:
                path.append(expl[state][1])
                state = expl[state][0]

            # print(path[::-1])

            return path[::-1]
        
        else:
            for s, a, c in problem.getSuccessors(state):
                # path_cost = util.manhattanDistance(state, strt_state) + heuristic(state, problem)
                # est_cost = cost + 1 + heuristic(s, problem)
                est_cost = cost + problem.getCostOfActions([a]) + heuristic(s, problem)

                if not ((est_cost > cost) and (s in expl)):
                    front.update((s, state, a, est_cost), est_cost)
                    expl[s] = [state, a, est_cost]





    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

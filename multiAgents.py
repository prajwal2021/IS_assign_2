# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** TTU CS 5368 Fall 2025 YOUR CODE HERE ***"
        # Get all legal actions for Pacman (agent 0)
        legalActions = gameState.getLegalActions(0)
        if not legalActions:
            return Directions.STOP
        
        # Find the best action by evaluating each legal action
        bestAction = None
        bestValue = float('-inf')
        
        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            value = self.minimax(successor, 1, 0)  # Start with ghost 1, depth 0
            if value > bestValue:
                bestValue = value
                bestAction = action
        
        return bestAction
    
    def minimax(self, gameState, agentIndex, depth):
        """
        Recursive minimax helper function.
        agentIndex: 0 for Pacman (MAX), >0 for ghosts (MIN)
        depth: current depth in the search tree
        """
        # Base cases
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        if depth >= self.depth:
            return self.evaluationFunction(gameState)
        
        # Get legal actions for current agent
        legalActions = gameState.getLegalActions(agentIndex)
        if not legalActions:
            return self.evaluationFunction(gameState)
        
        # Determine next agent and depth
        numAgents = gameState.getNumAgents()
        nextAgent = agentIndex + 1
        nextDepth = depth
        
        # If current agent is the last ghost, next agent is Pacman and depth increases
        if nextAgent >= numAgents:
            nextAgent = 0
            nextDepth = depth + 1
        
        if agentIndex == 0:  # Pacman's turn (MAX player)
            maxValue = float('-inf')
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                value = self.minimax(successor, nextAgent, nextDepth)
                maxValue = max(maxValue, value)
            return maxValue
        else:  # Ghost's turn (MIN player)
            minValue = float('inf')
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                value = self.minimax(successor, nextAgent, nextDepth)
                minValue = min(minValue, value)
            return minValue

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** TTU CS 5368 Fall 2025 YOUR CODE HERE ***"
        # Get all legal actions for Pacman (agent 0)
        legalActions = gameState.getLegalActions(0)
        if not legalActions:
            return Directions.STOP
        
        # Find the best action by evaluating each legal action with alpha-beta pruning
        bestAction = None
        bestValue = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            value = self.alphaBeta(successor, 1, 0, alpha, beta)  # Start with ghost 1, depth 0
            if value > bestValue:
                bestValue = value
                bestAction = action
            alpha = max(alpha, value)
        
        return bestAction
    
    def alphaBeta(self, gameState, agentIndex, depth, alpha, beta):
        """
        Recursive alpha-beta pruning helper function.
        agentIndex: 0 for Pacman (MAX), >0 for ghosts (MIN)
        depth: current depth in the search tree
        alpha: best value for MAX player so far
        beta: best value for MIN player so far
        """
        # Base cases
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        if depth >= self.depth:
            return self.evaluationFunction(gameState)
        
        # Get legal actions for current agent
        legalActions = gameState.getLegalActions(agentIndex)
        if not legalActions:
            return self.evaluationFunction(gameState)
        
        # Determine next agent and depth
        numAgents = gameState.getNumAgents()
        nextAgent = agentIndex + 1
        nextDepth = depth
        
        # If current agent is the last ghost, next agent is Pacman and depth increases
        if nextAgent >= numAgents:
            nextAgent = 0
            nextDepth = depth + 1
        
        if agentIndex == 0:  # Pacman's turn (MAX player)
            v = float('-inf')
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                value = self.alphaBeta(successor, nextAgent, nextDepth, alpha, beta)
                v = max(v, value)
                if v > beta:  # Alpha-beta pruning
                    return v
                alpha = max(alpha, v)
            return v
        else:  # Ghost's turn (MIN player)
            v = float('inf')
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                value = self.alphaBeta(successor, nextAgent, nextDepth, alpha, beta)
                v = min(v, value)
                if v < alpha:  # Alpha-beta pruning
                    return v
                beta = min(beta, v)
            return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** TTU CS 5368 Fall 2025 YOUR CODE HERE ***"
        # Get all legal actions for Pacman (agent 0)
        legalActions = gameState.getLegalActions(0)
        if not legalActions:
            return Directions.STOP
        
        # Find the best action by evaluating each legal action
        bestAction = None
        bestValue = float('-inf')
        
        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            value = self.expectimax(successor, 1, 0)  # Start with ghost 1, depth 0
            if value > bestValue:
                bestValue = value
                bestAction = action
        
        return bestAction
    
    def expectimax(self, gameState, agentIndex, depth):
        """
        Recursive expectimax helper function.
        agentIndex: 0 for Pacman (MAX), >0 for ghosts (CHANCE)
        depth: current depth in the search tree
        """
        # Base cases
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        if depth >= self.depth:
            return self.evaluationFunction(gameState)
        
        # Get legal actions for current agent
        legalActions = gameState.getLegalActions(agentIndex)
        if not legalActions:
            return self.evaluationFunction(gameState)
        
        # Determine next agent and depth
        numAgents = gameState.getNumAgents()
        nextAgent = agentIndex + 1
        nextDepth = depth
        
        # If current agent is the last ghost, next agent is Pacman and depth increases
        if nextAgent >= numAgents:
            nextAgent = 0
            nextDepth = depth + 1
        
        if agentIndex == 0:  # Pacman's turn (MAX player)
            maxValue = float('-inf')
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                value = self.expectimax(successor, nextAgent, nextDepth)
                maxValue = max(maxValue, value)
            return maxValue
        else:  # Ghost's turn (CHANCE player)
            # Calculate expected value: sum of all successor values / number of actions
            totalValue = 0
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                value = self.expectimax(successor, nextAgent, nextDepth)
                totalValue += value
            
            # All actions are equally likely (uniform probability)
            expectedValue = totalValue / len(legalActions)
            return expectedValue



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
        # Check available moves for Pacman
        availableMoves = gameState.getLegalActions(0)
        if len(availableMoves) == 0:
            return Directions.STOP
        
        # Initialize tracking variables for optimal move selection
        optimalMove = None
        highestScore = float('-inf')
        
        # Evaluate each possible move to find the best one
        for move in availableMoves:
            nextState = gameState.generateSuccessor(0, move)
            moveScore = self.evaluateMove(nextState, 1, 0)  # Begin with first ghost
            if moveScore > highestScore:
                highestScore = moveScore
                optimalMove = move
        
        return optimalMove
    
    def evaluateMove(self, state, currentAgent, currentDepth):
        """
        Recursive evaluation function implementing minimax algorithm.
        currentAgent: 0 represents Pacman (seeks maximum), >0 represents ghosts (seek minimum)
        currentDepth: tracks how deep we are in the search tree
        """
        # Handle terminal conditions first
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        
        # Stop searching if we've reached maximum depth
        if currentDepth >= self.depth:
            return self.evaluationFunction(state)
        
        # Get possible actions for the current agent
        possibleActions = state.getLegalActions(currentAgent)
        if len(possibleActions) == 0:
            return self.evaluationFunction(state)
        
        # Calculate which agent moves next and whether depth should increase
        totalAgents = state.getNumAgents()
        nextAgent = currentAgent + 1
        newDepth = currentDepth
        
        # When we've gone through all ghosts, it's Pacman's turn again and depth increases
        if nextAgent >= totalAgents:
            nextAgent = 0
            newDepth = currentDepth + 1
        
        if currentAgent == 0:  # Pacman's move (MAXIMIZER)
            bestScore = float('-inf')
            for action in possibleActions:
                newState = state.generateSuccessor(currentAgent, action)
                score = self.evaluateMove(newState, nextAgent, newDepth)
                bestScore = max(bestScore, score)
            return bestScore
        else:  # Ghost's move (MINIMIZER)
            worstScore = float('inf')
            for action in possibleActions:
                newState = state.generateSuccessor(currentAgent, action)
                score = self.evaluateMove(newState, nextAgent, newDepth)
                worstScore = min(worstScore, score)
            return worstScore

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** TTU CS 5368 Fall 2025 YOUR CODE HERE ***"
        # Retrieve possible moves for Pacman
        moveOptions = gameState.getLegalActions(0)
        if len(moveOptions) == 0:
            return Directions.STOP
        
        # Set up variables for finding optimal move with pruning
        chosenMove = None
        topScore = float('-inf')
        lowerBound = float('-inf')
        upperBound = float('inf')
        
        # Test each move and apply alpha-beta optimization
        for move in moveOptions:
            resultingState = gameState.generateSuccessor(0, move)
            moveValue = self.searchWithPruning(resultingState, 1, 0, lowerBound, upperBound)
            if moveValue > topScore:
                topScore = moveValue
                chosenMove = move
            lowerBound = max(lowerBound, moveValue)
        
        return chosenMove
    
    def searchWithPruning(self, state, agent, depth, alpha, beta):
        """
        Implements minimax with alpha-beta pruning for efficiency.
        agent: 0 for Pacman (maximizer), >0 for ghosts (minimizer)
        depth: current search depth
        alpha: best score for maximizer so far
        beta: best score for minimizer so far
        """
        # Check for game-ending conditions
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        
        # Stop if we've reached the search limit
        if depth >= self.depth:
            return self.evaluationFunction(state)
        
        # Get valid moves for current agent
        validMoves = state.getLegalActions(agent)
        if len(validMoves) == 0:
            return self.evaluationFunction(state)
        
        # Determine next player and depth progression
        agentCount = state.getNumAgents()
        followingAgent = agent + 1
        updatedDepth = depth
        
        # After all ghosts move, it's Pacman's turn and we go deeper
        if followingAgent >= agentCount:
            followingAgent = 0
            updatedDepth = depth + 1
        
        if agent == 0:  # Pacman's turn (MAXIMIZER)
            currentBest = float('-inf')
            for move in validMoves:
                newState = state.generateSuccessor(agent, move)
                moveScore = self.searchWithPruning(newState, followingAgent, updatedDepth, alpha, beta)
                currentBest = max(currentBest, moveScore)
                if currentBest > beta:  # Prune unnecessary branches
                    return currentBest
                alpha = max(alpha, currentBest)
            return currentBest
        else:  # Ghost's turn (MINIMIZER)
            currentWorst = float('inf')
            for move in validMoves:
                newState = state.generateSuccessor(agent, move)
                moveScore = self.searchWithPruning(newState, followingAgent, updatedDepth, alpha, beta)
                currentWorst = min(currentWorst, moveScore)
                if currentWorst < alpha:  # Prune unnecessary branches
                    return currentWorst
                beta = min(beta, currentWorst)
            return currentWorst

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
        # Check what moves Pacman can make
        pacmanMoves = gameState.getLegalActions(0)
        if len(pacmanMoves) == 0:
            return Directions.STOP
        
        # Initialize variables to track the best move
        selectedMove = None
        maximumScore = float('-inf')
        
        # Analyze each possible move to determine the best choice
        for move in pacmanMoves:
            futureState = gameState.generateSuccessor(0, move)
            moveScore = self.calculateExpectedValue(futureState, 1, 0)  # Start with first ghost
            if moveScore > maximumScore:
                maximumScore = moveScore
                selectedMove = move
        
        return selectedMove
    
    def calculateExpectedValue(self, state, agent, depth):
        """
        Recursive function implementing expectimax algorithm.
        agent: 0 for Pacman (maximizer), >0 for ghosts (chance nodes)
        depth: current level in the search tree
        """
        # Handle end-game scenarios
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        
        # Stop searching when we reach the depth limit
        if depth >= self.depth:
            return self.evaluationFunction(state)
        
        # Get available actions for the current agent
        availableActions = state.getLegalActions(agent)
        if len(availableActions) == 0:
            return self.evaluationFunction(state)
        
        # Figure out which agent moves next and depth progression
        totalAgents = state.getNumAgents()
        nextAgent = agent + 1
        newDepth = depth
        
        # When all ghosts have moved, it's Pacman's turn and depth increases
        if nextAgent >= totalAgents:
            nextAgent = 0
            newDepth = depth + 1
        
        if agent == 0:  # Pacman's turn (MAXIMIZER)
            bestOutcome = float('-inf')
            for action in availableActions:
                nextState = state.generateSuccessor(agent, action)
                outcome = self.calculateExpectedValue(nextState, nextAgent, newDepth)
                bestOutcome = max(bestOutcome, outcome)
            return bestOutcome
        else:  # Ghost's turn (CHANCE NODE)
            # Compute the average value across all possible ghost actions
            sumOfOutcomes = 0
            for action in availableActions:
                nextState = state.generateSuccessor(agent, action)
                outcome = self.calculateExpectedValue(nextState, nextAgent, newDepth)
                sumOfOutcomes += outcome
            
            # Since ghosts choose randomly, we take the average
            averageOutcome = sumOfOutcomes / len(availableActions)
            return averageOutcome



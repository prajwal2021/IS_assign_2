# CS5368 Multi-Agent Pacman Project

## Project Overview
This project implements three different AI agents for the classic Pacman game using adversarial search algorithms. The goal is to create intelligent agents that can make optimal decisions when facing multiple opponents (ghosts) in a dynamic environment.

## Implemented Agents

### 1. MinimaxAgent
**What it does:** This agent uses the minimax algorithm to find the best move by considering all possible future game states.

**How it works:**
- Pacman (agent 0) tries to maximize his score
- Ghosts (agents 1, 2, 3...) try to minimize Pacman's score
- The algorithm looks ahead a certain number of moves (depth) and picks the move that leads to the best possible outcome

**Key features:**
- Uses `evaluateMove()` method to recursively analyze game states
- Handles multiple agents with proper turn management
- Stops searching when reaching maximum depth or game-ending conditions

### 2. AlphaBetaAgent
**What it does:** This is an optimized version of minimax that uses alpha-beta pruning to eliminate unnecessary calculations.

**How it works:**
- Same logic as minimax but with smart pruning
- Uses `searchWithPruning()` method with alpha and beta bounds
- Skips evaluating branches that won't affect the final decision
- Much faster than regular minimax while giving identical results

**Key features:**
- Implements `lowerBound` and `upperBound` for pruning
- Maintains same multi-agent logic as minimax
- Significantly reduces computation time

### 3. ExpectimaxAgent
**What it does:** This agent treats ghosts as random players rather than perfect minimizers, making it more realistic for actual gameplay.

**How it works:**
- Pacman still tries to maximize his score
- Ghosts are modeled as chance nodes that choose moves randomly
- Calculates expected value by averaging all possible ghost outcomes
- More realistic since real ghosts don't always make optimal moves

**Key features:**
- Uses `calculateExpectedValue()` method for expected value computation
- Treats ghosts as chance nodes with uniform probability
- More suitable for games against non-optimal opponents

## Technical Implementation Details

### Multi-Agent Turn Management
The implementation handles the complex turn sequence:
1. Pacman moves first (agent 0)
2. Ghost 1 moves (agent 1)
3. Ghost 2 moves (agent 2)
4. ... and so on
5. After all agents move, depth increases and it's Pacman's turn again

### Depth Management
- Each "depth" represents one complete round of all agents
- The search stops when reaching the specified depth limit
- Terminal states (win/lose) also stop the search

### Evaluation Function
All agents use the same evaluation function that returns the game score, but this can be customized for better performance.

## Code Structure

### MinimaxAgent
```python
def getAction(self, gameState):
    # Get available moves and find the best one
    availableMoves = gameState.getLegalActions(0)
    # Evaluate each move and select the optimal choice
    
def evaluateMove(self, state, currentAgent, currentDepth):
    # Recursive minimax implementation
    # Handles MAX nodes (Pacman) and MIN nodes (ghosts)
```

### AlphaBetaAgent
```python
def getAction(self, gameState):
    # Similar to minimax but with pruning bounds
    # Uses lowerBound and upperBound for optimization
    
def searchWithPruning(self, state, agent, depth, alpha, beta):
    # Implements alpha-beta pruning
    # Prunes branches that won't affect the final decision
```

### ExpectimaxAgent
```python
def getAction(self, gameState):
    # Finds best move considering random ghost behavior
    
def calculateExpectedValue(self, state, agent, depth):
    # Computes expected value for chance nodes
    # Averages all possible ghost outcomes
```

## Common Questions and Answers

### Q: Why do we need different algorithms?
**A:** Each algorithm is suited for different scenarios:
- **Minimax**: Best when opponents play optimally
- **Alpha-Beta**: Same as minimax but much faster
- **Expectimax**: Better when opponents make random or suboptimal moves

### Q: How does the multi-agent system work?
**A:** The game follows a strict turn order:
1. All agents get to move once per round
2. Depth increases after each complete round
3. The algorithm tracks which agent's turn it is and what the next agent should be

### Q: What's the difference between minimax and expectimax?
**A:** 
- **Minimax**: Assumes opponents will always make the worst possible move for you
- **Expectimax**: Assumes opponents make random moves, so it calculates the average outcome

### Q: Why is alpha-beta pruning useful?
**A:** Alpha-beta pruning eliminates branches that won't change the final decision, making the search much faster without affecting the result.

### Q: How do I choose the right depth?
**A:** Deeper search gives better decisions but takes more time. A depth of 2-4 is usually a good balance between performance and decision quality.

### Q: What happens if there are no legal moves?
**A:** The agent returns `Directions.STOP` as a fallback when no moves are available.

### Q: How does the evaluation function work?
**A:** The default evaluation function returns the game score, but you can create custom functions that consider factors like:
- Distance to food
- Distance to ghosts
- Number of dots remaining
- Power pellet status

## Running the Code

To test the agents, use the provided test scripts:
```bash
python3 pacman.py -p MinimaxAgent
python3 pacman.py -p AlphaBetaAgent  
python3 pacman.py -p ExpectimaxAgent
```

## Performance Considerations

- **Minimax**: Complete but slow for deep searches
- **Alpha-Beta**: Much faster, identical results to minimax
- **Expectimax**: Good balance of speed and realistic gameplay

## Future Improvements

Potential enhancements could include:
- Custom evaluation functions
- Transposition tables for caching
- Iterative deepening
- Better heuristics for ghost behavior

## Learning Outcomes

This project demonstrates:
- Adversarial search algorithms
- Multi-agent systems
- Game tree search optimization
- Probability and expected value calculations
- Recursive algorithm design

The implementation shows how different assumptions about opponent behavior lead to different optimal strategies, which is crucial for AI systems that must operate in uncertain environments.

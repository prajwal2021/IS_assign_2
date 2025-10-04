# CS5368 Multi-Agent Pacman Project - Implementation Analysis

## Basic Questions:

### 1. What is your implementation strategy for Question 1 (MiniMax)? Explain.

**My implementation strategy for MiniMax:**

I used a recursive approach with two main methods:
- `getAction()`: Handles the top-level decision making for Pacman
- `evaluateMove()`: Recursively explores the game tree

**Key strategy elements:**
- **Multi-agent handling**: I track which agent's turn it is (0 for Pacman, >0 for ghosts)
- **Depth management**: After all agents move once, the depth increases and it's Pacman's turn again
- **Turn-based logic**: Pacman (agent 0) maximizes scores, while ghosts (agents 1,2,3...) minimize scores
- **Base cases**: Stop recursion at terminal states (win/lose) or when reaching maximum depth

The algorithm evaluates each possible move by looking ahead through all possible ghost responses, then picks the move that leads to the best outcome assuming optimal play from both sides.

### 2. What is your implementation strategy for Question 2 (AlphaBeta Pruning)? Explain.

**My implementation strategy for AlphaBeta Pruning:**

I built upon the MiniMax foundation but added pruning optimization:
- `getAction()`: Same top-level logic as MiniMax
- `searchWithPruning()`: Recursive function with alpha-beta bounds

**Key strategy elements:**
- **Pruning bounds**: Uses `lowerBound` (alpha) and `upperBound` (beta) to track best scores
- **Early termination**: Stops exploring branches when `currentBest > beta` (MAX) or `currentWorst < alpha` (MIN)
- **Bound updates**: Continuously updates alpha/beta values during search
- **Same multi-agent logic**: Maintains identical turn management as MiniMax

The pruning eliminates branches that won't affect the final decision, making it much faster while producing identical results to MiniMax.

### 3. What is your implementation strategy for Question 3 (ExpectiMax)? Explain.

**My implementation strategy for ExpectiMax:**

I modified the MiniMax approach to handle probabilistic ghost behavior:
- `getAction()`: Same top-level decision making
- `calculateExpectedValue()`: Recursive function treating ghosts as chance nodes

**Key strategy elements:**
- **Chance nodes**: Ghosts are modeled as random players, not optimal minimizers
- **Expected value calculation**: Computes average outcome across all possible ghost actions
- **Uniform probability**: Each ghost action has equal probability (1/number_of_actions)
- **Realistic gameplay**: More suitable for games against non-optimal opponents

The algorithm calculates the expected value by averaging all possible ghost outcomes, making it more realistic for actual gameplay scenarios.

## Advanced Questions:

### 1. What changes did you make to move your Question 1 solution to your Question 2 solution?

**Changes from MiniMax to AlphaBeta:**

1. **Method renaming**: `evaluateMove()` → `searchWithPruning()`
2. **Added pruning parameters**: Added `alpha` and `beta` parameters to track bounds
3. **Pruning conditions**: Added early termination checks:
   - For MAX nodes: `if currentBest > beta: return currentBest`
   - For MIN nodes: `if currentWorst < alpha: return currentWorst`
4. **Bound updates**: Continuously update alpha/beta during search
5. **Variable renaming**: Used `lowerBound`/`upperBound` instead of `alpha`/`beta` for clarity

**Core logic remained identical** - only added optimization without changing the fundamental algorithm.

### 2. What changes did you make to move your Question 1 solution to your Question 3 solution?

**Changes from MiniMax to ExpectiMax:**

1. **Method renaming**: `evaluateMove()` → `calculateExpectedValue()`
2. **Ghost behavior change**: Ghosts became chance nodes instead of minimizers
3. **Expected value calculation**: 
   - **Before**: `minValue = min(minValue, value)` (MIN logic)
   - **After**: `averageOutcome = sumOfOutcomes / len(availableActions)` (CHANCE logic)
4. **Variable updates**: 
   - `worstScore` → `sumOfOutcomes`
   - `minValue` → `averageOutcome`
5. **Comment updates**: Changed from "MINIMIZER" to "CHANCE NODE" descriptions

**Key conceptual change**: Ghosts now represent uncertainty rather than adversarial optimization, making the algorithm more suitable for realistic gameplay scenarios where opponents don't always play optimally.

## Implementation Summary

The three algorithms demonstrate different approaches to adversarial search:
- **MiniMax**: Complete but slow, assumes optimal opponents
- **AlphaBeta**: Same results as MiniMax but much faster through pruning
- **ExpectiMax**: More realistic for actual gameplay with probabilistic opponents

Each implementation maintains the same multi-agent turn management system while applying different decision-making strategies based on assumptions about opponent behavior.
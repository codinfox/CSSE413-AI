# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        import util
        mincost = 9999
        for food in newFood.asList():
            tmpdist = util.manhattanDistance(newPos, food)
            if tmpdist < mincost:
                mincost = tmpdist
        ghostCost = 0
        for ghostState in newGhostStates:
            if util.manhattanDistance(newPos, ghostState.getPosition()) <= 1:
                ghostCost += 50
        return successorGameState.getScore()*5 + 5/float(mincost) - ghostCost

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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          Directions.STOP:
            The stop direction, which is always legal

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        real_depth = self.depth
        evalfunc = self.evaluationFunction
        def minmax(state, depth, agentindex):
            bestmove = {"score": 0, "action": None}
            if state.isWin() or state.isLose() or depth == real_depth:
                bestmove["score"] = evalfunc(state)
                bestmove["action"] = None
                return bestmove
            if agentindex == 0: # pacman
                bestmove["score"] = -float("inf")
            else:
                bestmove["score"] = float("inf")

            if agentindex == state.getNumAgents()-1:
                depth += 1

            for action in state.getLegalActions(agentindex):
                next_state = state.generateSuccessor(agentindex, action)
                result = minmax(next_state, depth, (agentindex + 1) % state.getNumAgents())
                if agentindex == 0:
                    if result["score"] > bestmove["score"]:
                        bestmove["score"] = result["score"]
                        bestmove["action"] = action
                else:
                    if result["score"] < bestmove["score"]:
                        bestmove["score"] = result["score"]
                        bestmove["action"] = action

            return bestmove

        final_move = minmax(gameState, 0, 0)
        # print final_move["score"]
        return final_move["action"]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        real_depth = self.depth
        evalfunc = self.evaluationFunction
        def abminmax(state, depth, agentindex, alpha, beta):
            bestmove = {"score": 0, "action": None}
            if state.isWin() or state.isLose() or depth == real_depth:
                bestmove["score"] = evalfunc(state)
                bestmove["action"] = None
                return bestmove
            if agentindex == 0: # pacman
                bestmove["score"] = alpha
            else:
                bestmove["score"] = beta

            if agentindex == state.getNumAgents()-1:
                depth += 1

            for action in state.getLegalActions(agentindex):
                next_state = state.generateSuccessor(agentindex, action)
                result = abminmax(next_state, depth, (agentindex + 1) % state.getNumAgents(), alpha, beta)
                if agentindex == 0:
                    if result["score"] > bestmove["score"]:
                        bestmove["score"] = result["score"]
                        alpha = result["score"]
                        bestmove["action"] = action
                else:
                    if result["score"] < bestmove["score"]:
                        bestmove["score"] = result["score"]
                        beta = result["score"]
                        bestmove["action"] = action
                if alpha >= beta:
                    break

            return bestmove

        final_move = abminmax(gameState, 0, 0, -float("inf"), float("inf"))
        print final_move["score"]
        return final_move["action"]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        real_depth = self.depth
        evalfunc = self.evaluationFunction
        def expmax(state, depth, agentindex):
            bestmove = {"score": 0, "action": None}
            if state.isWin() or state.isLose() or depth == real_depth:
                bestmove["score"] = evalfunc(state)
                bestmove["action"] = None
                return bestmove
            if agentindex == 0: # pacman
                bestmove["score"] = -float("inf")
            else:
                bestmove["score"] = float("inf")

            if agentindex == state.getNumAgents()-1:
                depth += 1

            if agentindex == 0:
                for action in state.getLegalActions(agentindex):
                    next_state = state.generateSuccessor(agentindex, action)
                    result = expmax(next_state, depth, (agentindex + 1) % state.getNumAgents())
                    if result["score"] > bestmove["score"]:
                        bestmove["score"] = result["score"]
                        bestmove["action"] = action
            else:
                overall_estimate_result = 0
                for action in state.getLegalActions(agentindex):
                    next_state = state.generateSuccessor(agentindex, action)
                    result = expmax(next_state, depth, (agentindex + 1) % state.getNumAgents())
                    overall_estimate_result += result["score"]
                bestmove["score"] = overall_estimate_result / float(len(state.getLegalActions(agentindex)))
                bestmove["action"] = None
            return bestmove

        final_move = expmax(gameState, 0, 0)
        # print final_move["score"]
        return final_move["action"]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:
      This algorithm is inspired by <https://github.com/rahulrrixe/Multi-Agent-Pacman/blob/master/multiAgents.py>

      First, if the current state is winning, we need to definitely choose this state, therefore return inf.
      By doing so, I also eliminated the problem that the food list is empty.

      Then, we need to avoid to meet the ghosts. We consider the nearest ghost which is most likely to be met.
      Therefore, we need to find the distance to the nearest ghost. The *higher* the distance is, the safer the
      pacman can be.

      Next, we should encourage the pacman to eat pellets to fight with ghosts. Therefore, the longer fear time is,
      the better chance our pacman can win.

      We also want our pacman to always go to the area where food are densely located to enhance the chance and promote
      the efficiency of our pacman eating thosse food. And we want the distance to the nearest food to be small.

      Therefore, we arrive at the following solution.

      This solution is inspired by an online code. If we make the return statement be like:
            return fear_award + ghost_penalty - min_food_distance + currentGameState.getScore()
      and this will be my original implementation. The last experiment result of my own implementation is:
            Average Score: 811.7
            Scores:        1513, 4, 1042, 1311, 1173, 88, 228, 1002, 1467, 289
            Win Rate:      6/10 (0.60)
            Record:        Win, Loss, Win, Win, Win, Loss, Loss, Win, Win, Loss
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
        return float("inf")

    import util

    current_position = currentGameState.getPacmanPosition()
    ghost_distances = [util.manhattanDistance(current_position, ghost_position)
                       for ghost_position in currentGameState.getGhostPositions()]
    ghost_penalty = 0
    if len(ghost_distances) != 0:
        ghost_penalty = min(ghost_distances)

    fear_times = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]
    fear_award = sum(fear_times)

    sparse_penalty = 0
    food_distances = []
    for food in currentGameState.getFood().asList(): # inspired by others' codes
        neighborhood = [(food[0]+1, food[1]), (food[0], food[1]+1),
                        (food[0]-1, food[1]), (food[0], food[1]-1)]
        for neighbor in neighborhood:
            if (not currentGameState.hasWall(neighbor[0], neighbor[1]) and
                not currentGameState.hasFood(neighbor[0], neighbor[1])):
                sparse_penalty += 1
        food_distances.append(util.manhattanDistance(current_position, food))
    min_food_distance = 0
    if len(food_distances) != 0:
        min_food_distance = min(food_distances)

    return fear_award + ghost_penalty/(min_food_distance) + currentGameState.getScore() - sparse_penalty



# Abbreviation
better = betterEvaluationFunction


class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


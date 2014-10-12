# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.q_values = util.Counter()

        "*** YOUR CODE HERE ***"
        states = mdp.getStates()
        for iter in range(iterations):
            tmp_values = util.Counter()
            for state in states:
                actions = mdp.getPossibleActions(state)
                v_max_a = -float("inf")
                if state == "TERMINAL_STATE":
                    v_max_a = 0
                for action in actions:
                    trans_and_probs = mdp.getTransitionStatesAndProbs(state, action)
                    v_a = 0
                    for next_state, prob in trans_and_probs:
                        v_a += \
                            prob*(mdp.getReward(state, action, next_state)+self.discount*self.values[next_state])
                    if v_a > v_max_a:
                        v_max_a = v_a
                    self.q_values[(state, action)] = v_a
                tmp_values[state] = v_max_a
            self.values = tmp_values

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def getQValue(self, state, action):
        """
          The q-value of the state action pair
          (after the indicated number of value iteration
          passes).  Note that value iteration does not
          necessarily create this quantity and you may have
          to derive it on the fly.
        """
        "*** YOUR CODE HERE ***"
        return self.q_values[(state, action)]

    def getPolicy(self, state):
        """
          The policy is the best action in the given state
          according to the values computed by value iteration.
          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.mdp.getPossibleActions(state)
        best_q = -float("inf")
        best_action = None
        for action in actions:
            tmp_q = self.getQValue(state, action)
            if tmp_q > best_q:
                best_q = tmp_q
                best_action = action
        return best_action


    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.getPolicy(state)
  

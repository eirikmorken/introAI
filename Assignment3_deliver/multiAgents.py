from math import log

import sys

#from util import manhattanDistance
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
		self.current_depth = 0

# My code
class MinimaxAgent(MultiAgentSearchAgent):
	def getAction(self, gameState):
		not_used, max_action = self.minimaxDecision(gameState, self.index, 0)
		return max_action

	# The three following functions cooresponds respectevly to the ones in fig. 5.3
	def minimaxDecision(self, state, agent, d):
		agents = state.getNumAgents()

		if d == self.depth and agent % agents == 0: return self.evaluationFunction(state), None

		if agent % agents == 0: return self.maxValue(state, agent % agents, d)

		return self.minValue(state, agent % agents, d)

	def maxValue(self, state, agent, d):
		succ_states = [(state.generateSuccessor(agent, a), a) for a in state.getLegalActions(agent)]

		if len(succ_states) == 0: return self.evaluationFunction(state), None

		val = -sys.maxint
		val_action = None

		new_agent = agent + 1
		new_d = d + 1
		for succ_state, a in succ_states:
			new_value, new_a = self.minimaxDecision(succ_state, new_agent, new_d)
			if new_value > val:
				val = new_value
				val_action = a

		return val, val_action

	def minValue(self, state, agent, d):
		succ_states = [(state.generateSuccessor(agent, a), a) for a in state.getLegalActions(agent)]

		if len(succ_states) == 0: return self.evaluationFunction(state), None

		val = sys.maxint
		val_action = None

		new_agent = agent + 1
		for succ_state, a in succ_states:
			new_value, new_a = self.minimaxDecision(succ_state, new_agent, d)
			if new_value < val:
				val = new_value
				val_action = a

		return val, val_action

class AlphaBetaAgent(MultiAgentSearchAgent):

	def getAction(self, gameState):
		not_used, max_action = self.alphaBetaSearch(gameState, self.index, 0, -sys.maxint, sys.maxint)
		return max_action

	# The three following functions cooresponds respectevly to the ones in fig. 5.7
	def alphaBetaSearch(self, state, agent, d, a, b):
		agents = state.getNumAgents()

		if d == self.depth and agent % agents == 0: return self.evaluationFunction(state), None

		if agent % agents == 0:
			return self.maxValue(state, agent % agents, d, a, b)

		return self.minValue(state, agent % agents, d, a, b)

	def maxValue(self, state, agent, d, a, b):
		leg_acts = state.getLegalActions(agent)
		if len(leg_acts) == 0: return self.evaluationFunction(state), None

		val = -sys.maxint
		val_act = None

		new_agent = agent + 1
		new_d = d + 1
		for act in leg_acts:
			succ_state = state.generateSuccessor(agent, act)
			new_val, new_act= self.alphaBetaSearch(succ_state, new_agent, new_d, a, b)
			if new_val > val:
				val = new_val
				val_act = act
			if val > b:
				return val, val_act
			a = max(a, val)

		return val, val_act

	def minValue(self, state, agent, d, a, b):
		leg_acts = state.getLegalActions(agent)

		if len(leg_acts) == 0: return self.evaluationFunction(state), None

		val = sys.maxint
		val_act = None

		new_agent = agent + 1
		for act in leg_acts:
			succ_state = state.generateSuccessor(agent, act)
			new_val, new_a = self.alphaBetaSearch(succ_state, new_agent, d, a, b)
			if new_val < val:
				val = new_val
				val_act = act
			if val < a:
				return val, val_act
			b = min(b, val)

		return val, val_act


import numpy as np

MODEL_SHAPE = [6, 2]

WINNER_RATIO = 2
EVOLUTION_RATE = 1/50

# TOOD # functions ----------------------
def initialization(*shape):
	return np.random.normal(size=shape) / 100
def sigmoidActivation(z):
	return np.exp(-np.logaddexp(0, -z))

def straightLineFitness(state):
	return state[:, 0] - 3 * np.abs(250 - state[:, 1])
def modification(shape):
	a = initialization(*shape) * EVOLUTION_RATE
	return a

class Agents:
	def __init__(self, numPlanes):
		self.weights = [initialization(numPlanes, to, fron) for (fron, to) in zip(MODEL_SHAPE, MODEL_SHAPE[1:])]
		self.biases = [initialization(numPlanes, s) for s in MODEL_SHAPE[1:]]
		self.resetScore()
	def resetScore(self):
		self.score = np.zeros(self.weights[0].shape[0])

	def forward(self, state):
		assert (shape := [w.shape[1] for w in self.weights]) == MODEL_SHAPE[1:], f'Unexpected model shape: {[self.weights[0].shape[2]]+shape}'
		self.score += straightLineFitness(state)
		for weight, bias in zip(self.weights, self.biases):
			z = weight * state[:, np.newaxis]
			z = np.sum(z, -1) + bias
			state = sigmoidActivation(z)
		return state

	def evolveField(self, field, keys):
		chosen = field[keys]
		assert nextGen.shape == field.shape
		return nextGen
	def evolve(self):
		winnerCount = self.score.size // WINNER_RATIO
		keys = np.argsort(self.score)[self.score.size - winnerCount:]
		self.resetScore()
		for i in range(len(MODEL_SHAPE) - 1):
			self.weights[i] = self.evolveField(self.weights[i], keys)
			self.biases[i]  = self.evolveField(self.biases[i], keys)

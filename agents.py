import numpy as np

MODEL_SHAPE = [6, 2]

WINNER_RATIO = 2
EVOLUTION_RATE = 1/20
EVOLUTION_CHANCE = 1/4

# functions ----------------------
def initialization(*shape):
	return np.random.normal(size=shape)
def sigmoidActivation(z):
	return np.exp(-np.logaddexp(0, -z))

def straightLineFitness(state):
	return state[:, 0] - 3 * np.abs(2.5 - state[:, 1])
def sawtoothModulo(x):
	mod = x / 4
	return mod - np.floor(mod) - 0.5
def sawtoothFitness(state):
	y = np.abs(state[:, 6]) + 3
	return state[:, 0] - 15 * np.abs(y - state[:, 1])
def modification(shape):
	a = initialization(*shape) * EVOLUTION_RATE
	a = a * (np.random.uniform(size=shape) < EVOLUTION_CHANCE)
	return a

class Agents:
	def __init__(self, numPlanes):
		self.weights = [initialization(numPlanes, to, fron) for (fron, to) in zip(MODEL_SHAPE, MODEL_SHAPE[1:])]
		self.biases = [initialization(numPlanes, s) for s in MODEL_SHAPE[1:]]
		self.resetScore()
	def resetScore(self):
		assert (shape := [w.shape[1] for w in self.weights]) == MODEL_SHAPE[1:], f'Unexpected model shape: {[self.weights[0].shape[2]]+shape}'
		self.score = np.zeros(self.weights[0].shape[0])

	def forward(self, state):
		state = np.concatenate((state, sawtoothModulo(state[:, 0])[:, np.newaxis]), axis=-1)
		self.score += sawtoothFitness(state)
		for weight, bias in zip(self.weights, self.biases):
			z = weight * state[:, np.newaxis]
			z = np.sum(z, -1) + bias
			state = sigmoidActivation(z)
		return state

	def evolveField(self, field, keys):
		chosen = field[keys]
		# TODO choose the new ones based on score
		nextGen = np.concatenate((chosen + modification(chosen.shape), chosen))
		assert nextGen.shape == field.shape
		return nextGen
	def evolve(self):
		winnerCount = self.score.size // WINNER_RATIO
		keys = np.argsort(self.score)[self.score.size - winnerCount:]
		print(np.max(self.score))
		self.resetScore()
		for i in range(len(MODEL_SHAPE) - 1):
			self.weights[i] = self.evolveField(self.weights[i], keys)
			self.biases[i]  = self.evolveField(self.biases[i], keys)

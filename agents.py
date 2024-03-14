import numpy as np

MODEL_SHAPE = (6, 10, 5, 2)

# TOOD # functions ----------------------
def initialization(*shape):
	return np.random.normal(size=shape)
def sigmoidActivation(z):
	return np.exp(-np.logaddexp(0, -z))

class Agents:
	def __init__(self, numPlanes):
		self.weights = [initialization(numPlanes, to, fron) for (fron, to) in zip(MODEL_SHAPE, MODEL_SHAPE[1:])]
		self.biases = [initialization(numPlanes, s) for s in MODEL_SHAPE[1:]]

	def forward(self, input):
		a = input
		for weight, bias in zip(self.weights, self.biases):
			z = weight * a[:, np.newaxis]
			z = np.sum(z, -1) + bias
			a = sigmoidActivation(z)
		return a


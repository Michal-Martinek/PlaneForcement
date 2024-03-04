import numpy as np

NUM_PLANES = 1
GRAVITY = 5.
ENGINE_ACCEL = 3.

class Simulation:
	def __init__(self):
		self.positions = np.repeat(np.array((0., 300.))[np.newaxis], NUM_PLANES, 0)
		self.speeds = np.zeros((NUM_PLANES, 2))

	def update(self, timedelta=1/60):
		self.positions += self.speeds * timedelta
		self.speeds += np.array((ENGINE_ACCEL, GRAVITY)) * timedelta

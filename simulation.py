import numpy as np
import pygame

NUM_PLANES = 1
GRAVITY = 5.
ENGINE_ACCEL = 3.
LIFT_COEFF = 0.2
LIFT_LEVER_COEFF = 0.0001
DRAG_COEFF = 0.1
ANGULAR_DRAG_COEFF = 0.03
ELEVATOR_MAX_ANGLE = 0.4 # ~ 23 degrees
ELEVATOR_LEVER_COEFF = 0.2

class Simulation:
	def __init__(self):
		self.positions = np.repeat(np.array((100., 300.))[np.newaxis], NUM_PLANES, 0)
		self.speeds = np.zeros((NUM_PLANES, 2))
		self.angles = np.zeros(NUM_PLANES)
		self.angularVels = np.zeros(NUM_PLANES)

	def update(self, timedelta, controlInputs, *, drawVectors=True):
		self.positions += self.speeds * timedelta
		self.speeds[:, 1] += GRAVITY * timedelta
		self.speeds += timedelta * (enginePower := self.rotate((ENGINE_ACCEL, 0)) * controlInputs[0])

		self.speeds += timedelta * (liftVec := self.rotate((0, -LIFT_COEFF)) * self.airflowSpeed()[:, np.newaxis] ** 2)
		self.speeds -= timedelta * (dragVec := DRAG_COEFF * self.speeds * np.linalg.norm(self.speeds, axis=1))

		self.angularVels -= ELEVATOR_LEVER_COEFF * timedelta * np.sin(controlInputs[1] * ELEVATOR_MAX_ANGLE * 2 - ELEVATOR_MAX_ANGLE)

		self.angles += self.angularVels * timedelta
		self.angularVels -= timedelta * LIFT_LEVER_COEFF * self.airflowSpeed() ** 2
		self.angularVels -= ANGULAR_DRAG_COEFF * timedelta * self.angularVels * np.abs(self.angularVels)

		if drawVectors:
			self.drawVec(6 * self.speeds)
			self.drawVec(15 * enginePower, (0, 255, 0))
			self.drawVec(6 * self.rotate((self.airflowSpeed()[0], 0)), (255, 255, 255))
			self.drawVec(15 * liftVec, (0, 255, 255))
			self.drawVec(-6 * dragVec, (0, 0, 255))

	def airflowSpeed(self):
		'''speed of airflow around wings'''
		coords = self.rotate((1, 0)) * self.speeds
		return np.sum(coords, -1)
	def rotate(self, vecs) -> np.ndarray:
		if isinstance(vecs, tuple): vecs = np.repeat(np.array((vecs,)), NUM_PLANES, 0)
		rotMat = np.moveaxis(np.array( ((np.cos(self.angles), np.sin(self.angles)), (-np.sin(self.angles), np.cos(self.angles))) ), -1, 0)
		product = rotMat * vecs[:, np.newaxis]
		return np.sum(product, -1)

	def drawVec(self, vec, color=(255, 0, 0)):
		while len(vec.shape) > 1: vec = vec[0]
		line = self.positions[0], (self.positions[0] + vec)
		pygame.draw.line(pygame.display.get_surface(), color, *line)

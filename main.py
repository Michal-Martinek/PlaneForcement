import time
import numpy as np
import pygame

from simulation import Simulation
from agents import Agents

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
FPS = 30
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

PLANE_IMG = pygame.image.load('Assets/bluePlane.png').convert()
PLANE_IMG.set_colorkey((255, 255, 255))

NUM_PLANES = 7

# helpers --------------------------
startTime = time.time()
def timedelta() -> float:
	global startTime
	prev = startTime
	startTime = time.time()
	return startTime - prev

def draw(simulation: Simulation):
	for pos, angle in zip(simulation.positions, simulation.angles * 180 / np.pi):
		img = pygame.transform.rotate(PLANE_IMG, angle)
		rect = img.get_rect()
		rect.center = pos
		display.blit(img, rect)

def mainLoop():
	simulation = Simulation(NUM_PLANES)
	agents = Agents(NUM_PLANES)

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					simulation = Simulation(NUM_PLANES)

		screenInputs = np.array(pygame.mouse.get_pos()) / (SCREEN_WIDTH, SCREEN_HEIGHT)
		screenInputs[1] = 1 - screenInputs[1]

		controlInputs = agents.forward(simulation.state())
		controlInputs[0] = screenInputs
		simulation.update(timedelta(), controlInputs)

		display.fill((0, 0, 0))
		draw(simulation)
		pygame.display.update()
		pygame.time.Clock().tick(FPS)
	
if __name__ == '__main__':
	mainLoop()

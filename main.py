import time
import numpy as np
import pygame

from simulation import Simulation

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
FPS = 30

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

PLANE_IMG = pygame.image.load('Assets/bluePlane.png').convert()
PLANE_IMG.set_colorkey((255, 255, 255))

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
	simulation = Simulation()

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					simulation = Simulation()

		display.fill((0, 0, 0))
		draw(simulation)
		simulation.update(timedelta())

		pygame.display.update()
		pygame.time.Clock().tick(FPS)
	
if __name__ == '__main__':
	mainLoop()

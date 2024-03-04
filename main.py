import time
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
	for planePos in simulation.positions:
		display.blit(PLANE_IMG, planePos)

def mainLoop():
	simulation = Simulation()

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		simulation.update(timedelta())

		display.fill((0, 0, 0))
		draw(simulation)	
		pygame.display.update()
		pygame.time.Clock().tick(FPS)
	
if __name__ == '__main__':
	mainLoop()

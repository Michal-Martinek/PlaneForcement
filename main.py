import time
import numpy as np
import pygame
import pickle

from simulation import Simulation
from agents import Agents

# switches -------------------------
USER_INPUT = False
RENDER_SIMULATION = True

# globals --------------------------
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
FPS = 30
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

PLANE_IMG = pygame.image.load('Assets/bluePlane.png').convert()
PLANE_IMG.set_colorkey((255, 255, 255))

NUM_PLANES = 300

# helpers --------------------------
def loadAgents(filename='models/agents.bin') -> Agents:
	try:
		with open(filename, 'rb') as f:
			agents = pickle.load(f)
			agents.resetScore()
			assert agents.weights[0].shape[0] == NUM_PLANES
			return agents
	except (FileNotFoundError, pickle.PickleError): pass
	except AssertionError as e: print(str(e))
	return Agents(NUM_PLANES)
def saveAgents(agents, filename='models/agents.bin'):
	with open(filename, 'wb') as f:
		pickle.dump(agents, f)

# globals ----------------------------
simulation = Simulation(NUM_PLANES)
agents = loadAgents()

# UI ---------------------------------
startTime = time.time()
def timedelta() -> float:
	global startTime
	prev = startTime
	startTime = time.time()
	return startTime - prev

def drawPlanes():
	for pos, angle in zip(simulation.positions, simulation.angles * 180 / np.pi):
		if np.abs(pos).sum() > 3 * SCREEN_WIDTH: continue
		img = pygame.transform.rotate(PLANE_IMG, angle)
		rect = img.get_rect()
		rect.center = pos
		display.blit(img, rect)
def drawSawtoothLine():
	for i in range(4):
		pygame.draw.line(display, (255, 0, 0), (400*i, 350), (200 + 400*i, 300))
		pygame.draw.line(display, (255, 0, 0), (200 + 400*i, 300), (400 + 400*i, 350))
def draw():
	display.fill((0, 0, 0))
	drawSawtoothLine()
	drawPlanes()
def updateUI():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				simulation.reset(NUM_PLANES)
	pygame.display.update()
	pygame.time.Clock().tick(FPS)

def getControlInputs():
	controlInputs = agents.forward(simulation.state())
	if USER_INPUT:
		userInput = np.array(pygame.mouse.get_pos()) / (SCREEN_WIDTH, SCREEN_HEIGHT)
		userInput[1] = 1 - userInput[1]
		controlInputs[0] = userInput
	return controlInputs

def testGeneration(duration):
	simStep = 0
	while simStep < duration:
		simStep += (delta := timedelta() if RENDER_SIMULATION else 1/FPS)
		forceLines = simulation.update(delta, getControlInputs())
		if RENDER_SIMULATION:
			draw()
			for l in forceLines: pygame.draw.line(display, *l)
			updateUI()

def mainLoop():
	running = True
	duration = 60
	while running:
		testGeneration(duration)
		saveAgents(agents)
		draw()
		updateUI()
		agents.evolve()
		simulation.reset(NUM_PLANES)

if __name__ == '__main__':
	mainLoop()

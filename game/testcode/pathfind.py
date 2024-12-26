import pygame
import numpy as np
from collections import deque

width=900
height=900

pygame.init()

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()


run = True

outOfBounds = [(0,500, 200, 600), (100, 500, 200, 800), (100, 700, 400, 800), (300, 300, 400, 800), (100, 300, 400, 400), (100, 100, 200, 400), (100, 100, 800, 200), (700, 100, 800, 400), (500, 300, 800, 400), (500, 300, 600, 800), (500, 700, 800, 800), (700, 500, 800, 800), (700, 500, 900, 600)]

stepSize = 50


def pathfind(start, end):
    start = (5*(np.floor(start[0]/50)), 50*(np.floor(start[1]/50)))
    end = (50*(np.floor(end[0]/50)), 50*(np.floor(end[1]/50)))

    possibleDir = [(-50, 0), (50, 0), (0, 50), (0, -50)]

    queue = deque([(start, [start])])  # Use deque for efficient popping
    visited = set()

    for bounds in outOfBounds:
        x1, y1, x2, y2 = bounds
        for x in range(x1, x2, 50):
            for y in range(y1, y2, 50):
                visited.add((x, y))

    while queue:
        current, path = queue.popleft()  # Faster O(1) pop from the left

        if current == end:
            return path
        
        if current in visited:
            continue

        visited.add(current)

        for direction in possibleDir:
            nextPos = (current[0] + direction[0], current[1] + direction[1])

            if 0 <= nextPos[0] < 50*(np.floor(width/50)) and 0 <= nextPos[1] < 50*(np.floor(height/50)) and nextPos not in visited:
                queue.append((nextPos, path + [nextPos]))

while run:
    screen.fill((150,150,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pass    

    for x in outOfBounds:
        pygame.draw.rect(screen, "BLACK", pygame.Rect(x[0], x[1], x[2]-x[0], x[3]-x[1]))

    paths = pathfind((0,0), pygame.mouse.get_pos())
    if paths:
        for path in paths:
            pygame.draw.rect(screen, "BLUE", pygame.Rect(path[0], path[1], 50, 50))



    for x in range(0, width, stepSize):
        for y in range(0, height, stepSize):
            pygame.draw.rect(screen, "BLACK", pygame.Rect(x, y, stepSize, stepSize), 1)
      

    pygame.display.flip()
pygame.quit()
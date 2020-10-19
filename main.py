from Game import Game
import pygame
import time
import datetime

useGraphics = True

pygame.init()

screen = pygame.display.set_mode((800, 800))

Game = Game(screen, 800, 800)
start = datetime.datetime.now()
for i in range(10000):
    for event in pygame.event.get():
        pass
    Game.tick()
    if useGraphics:
        screen.fill((0, 0, 0))
        Game.draw()
        screen.blit(pygame.transform.flip(screen, False, True), (0,0))
        pygame.display.flip()
        time.sleep(.01)
end = datetime.datetime.now()

print("elapsed time", end-start)
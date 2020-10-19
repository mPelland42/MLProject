import pygame
import GameConstants

class Obstacle:

    #spikes are location array LRUD
    def __init__(self, rect, spikes):
        self.rect, spikes = rect, spikes

    def tick(self):
        self.rect.x -= GameConstants.obstacleSpeed

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)
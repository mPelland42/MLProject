import GameConstants
import pygame


class Coin:
    def __init__(self, pos):
        self.posX = pos[0]
        self.posY = pos[1]

    def tick(self):
        self.posX -= GameConstants.coinSpeed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.posX, self.posY), GameConstants.coinSize)
    def __repr__(self):
        return "COIN: "+ str(self.posX) + " " + str(self.posY)
from GameConstants import gravity, tickTime, coinSize
import pygame
from RandomAgent import *

class Player:
    def __init__(self):
        self.y = 150
        self.x = 100
        self.v = 0
        self.radius = 50
        self.canJump = True

    def jump(self):
        self.v = 0.1

    def crouch(self):
        pass

    def tick(self, obstacles, coins, action):
        if action > 0 and self.canJump:
            self.v = action
        self.canJump = False
        oldY = self.y
        self.y += self.v*tickTime
        self.v -= gravity*tickTime
        if self.y < -self.radius:
            return -1
        #check for collisions against each obstacle
        for obstacle in obstacles:
            if obstacle.rect.left<= self.x and obstacle.rect.right >= self.x:
                if self.y >= obstacle.rect.top-self.radius and self.y <= obstacle.rect.bottom+self.radius:
                    #consult previous y
                    if oldY > obstacle.rect.bottom+self.radius:
                        self.y = obstacle.rect.bottom+self.radius+1
                        self.v = 0
                        self.canJump = True
                    else:
                        self.y = obstacle.rect.top-self.radius-1
                        self.v = 0
        reward = 0
        for coin in coins:
            if np.sqrt((self.x-coin.posX)**2 + (self.y - coin.posY)**2) < self.radius + coinSize:
                reward += 1
                coins.remove(coin)
        return reward


    def draw(self, screen):
        #print("I am at y", self.y)
        pygame.draw.circle(screen, (0, 0, 255), (self.x, int(self.y)), self.radius)
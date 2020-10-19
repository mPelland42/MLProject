from Player import Player
from Hole import Hole
from Obstacle import Obstacle
from GameConstants import *
import numpy as np
import pygame
from Coin import Coin

class GameState:

    def __init__(self, width, height):
        self.obstacles = []
        self.coins = []
        self.offset = 0 #for displaying and stuff
        self.player = Player()
        self.pageSize = (width, height)
        self.floorHeight = 50

        #generate a page
        self.obstacles.append(Obstacle(pygame.Rect(0, 0, width, groundHeight), []))

    def distance(self, a, b):
        return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

    def tick(self, action):
        for coin in self.coins:
            coin.tick()
        for obstacle in self.obstacles:
            obstacle.tick()
            if self.distance(obstacle.rect.topleft, (self.player.x, self.player.y)) < self.player.radius or self.distance(obstacle.rect.topleft, (self.player.x, self.player.y)) < self.player.radius:
                self.__init__(self.pageSize[0], self.pageSize[1])
                return -1

        reward = self.player.tick(self.obstacles, self.coins, action)
        if reward == -1:
            self.__init__(self.pageSize[0], self.pageSize[1])
            return reward
        self.cleanup()
        if self.allObstaclesOnScreen():
            self.generatePage()
        return reward

    def allObstaclesOnScreen(self):
        for obstacle in self.obstacles:
            if obstacle.rect.left > self.pageSize[1]:
                return False
        return True

    def generatePage(self):
        #randomly generate some number of platforms and holes, then make sure they are a certain distance from each other
        #if a platform is generated too close to another, don't generate it.
        for i in range(10):
            newPlatformRect = pygame.Rect(np.random.randint(self.pageSize[0], self.pageSize[0]*2), np.random.randint(self.floorHeight+50, self.pageSize[1]), np.random.randint(100, 500), np.random.randint(20, 100))
            addIt = True
            for obstacle in self.obstacles:
                xDist = abs(obstacle.rect.centerx - newPlatformRect.centerx) - obstacle.rect.width/2 - newPlatformRect.width/2
                yDist = abs(obstacle.rect.centery - newPlatformRect.centery) - obstacle.rect.height/2 - newPlatformRect.height/2
                if xDist + yDist < 200:
                    addIt = False
                    break
            if addIt:
                spikes = []  # self.makeSpikes(newPlatformRect)
                self.obstacles.append(Obstacle(newPlatformRect, spikes))

        if np.random.uniform() < 0.5:
            #generate hole
            holeWidth = np.random.randint(50, 200)
            holeCenter = np.random.randint(holeWidth/2+1, self.pageSize[0]-holeWidth/2-1)
            #make floor around hole
            self.obstacles.append(Obstacle(pygame.Rect((self.pageSize[0], 0), (self.pageSize[0]+holeCenter-holeWidth/2-self.pageSize[0], groundHeight)), []))
            self.obstacles.append(Obstacle(pygame.Rect((self.pageSize[0]+holeCenter+holeWidth/2, 0), (self.pageSize[0]*2-(self.pageSize[0]+holeCenter+holeWidth/2), groundHeight)), []))
        else:
            self.obstacles.append(Obstacle(pygame.Rect((self.pageSize[0], 0), (self.pageSize[0]*2, groundHeight)), []))
        #generate random coins, not intersecting platforms
        for i in range(5):
            addIt = True
            randomPos = (np.random.randint(0, self.pageSize[0]) + self.pageSize[0], np.random.randint(0, self.pageSize[1]))
            for obstacle in self.obstacles:
                if randomPos[1] >= obstacle.rect.top-coinSize and randomPos[1] <= obstacle.rect.bottom+coinSize:
                    if obstacle.rect.left <= randomPos[0] and obstacle.rect.right >= randomPos[0]:
                        addIt = False
                        break
            for coin in self.coins:
                if np.sqrt((randomPos[0]-coin.posX)**2 + (randomPos[1] - coin.posY)**2) <coinSize*2:
                    addIt = False
            if addIt:
                self.coins.append(Coin(randomPos))

    def makeSpikes(self, rect):
        pass

    def cleanup(self):
        for obstacle in self.obstacles:
            if obstacle.rect.right < 0:
                self.obstacles.remove(obstacle)
        for coin in self.coins:
            if coin.posX + coinSize/2 < 0:
                self.coins.remove(coin)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        for coin in self.coins:
            coin.draw(screen)
        self.player.draw(screen)
        #pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(0, 0, self.pageSize[0], groundHeight))
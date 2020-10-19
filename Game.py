from GameState import GameState
from RandomAgent import RandomAgent

class Game:

    def __init__(self, screen, width, height):
        self.gameState = GameState(width, height)
        self.screen = screen
        self.agent = RandomAgent()

    def tick(self):
        action = self.agent.getAction(self.gameState)
        gameStateStr = str(self.gameState)
        reward = self.gameState.tick(action)
        print(action, reward)#, gameStateStr, self.gameState)

    def draw(self):
        self.gameState.draw(self.screen)


import numpy as np

class RandomAgent():
    def __init__(self):
        pass
    def getAction(self, gameState):
        if (np.random.uniform() < 0.05):
            return np.random.uniform(5, 10)
        else:
            return 0
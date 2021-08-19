import random

class Deck:
    def __init__(self):
        self.cards = None
        self.reset()

    def shuffleDeck(self):
        self.reset()
        random.shuffle(self.cards)
    
    def drawCard(self):
        return self.cards.pop()

    def __str__(self):
        out = ""
        for card in self.cards:
            out = out + " " + card + ","
        return out

    def drawPyramid(self):
        pyramid = []
        while (len(pyramid) != 10):
            pyramid.append(self.drawCard())
        return pyramid

    
    def reset(self):
        self.cards = [
            'H7','H8','H9','H1','HU','HO','HK','HA',
            'G7','G8','G9','G1','GU','GO','GK','GA',
            'S7','S8','S9','S1','SU','SO','SK','SA',
            'E7','E8','E9','E1','EU','EO','EK','EA',
        ]



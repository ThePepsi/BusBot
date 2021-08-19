import os
import discord
from enum import Enum
from mGameCore.Deck import Deck

class Core:
    
    def __init__(self):
        self.games = []

    async def initGame(self, channel, host):
        game = Game(host,channel)
        self.games.append(game)
        
        txt = f'Willkommen bei BusBot. Jeder Mitspieler reagiert bitte mit einem Eigenen Emoji. Spieler {host.mention} das Spiel mit dem Emoji \U0001F504'
        m = await channel.send(txt)
        await m.add_reaction('\U0001F504')
         
        game.setStatus(GameStatus.LOGIN)
    
    async def joinGame(self, channel, player, emoji):
        game = next((game for game in self.games if game.isChannel(channel)), None)
        if game:
            game.playerJoin(player, emoji)

        print('Player: ' +str(player)+ ' joined')

    async def prepGame(self, user, channel):
        for game in self.games:
            if game.channel == channel and game.status != GameStatus.ENDED and game.hostUser == user:
                game.setStatus(GameStatus.PREP)
                txt = f'Und los Geht es! Karten werden ausgeteilt! \n Wenn jeder seine Karten hat bitte \U0001F504 drücken. \n Mittspieler sind:\n'
                for player in game.playerList:
                    txt = txt + f'{player.emoji} => {player.user}\n'
                m = await game.channel.send(txt)
                await m.add_reaction('\U0001F504')
                for p in game.prepGame():
                    txt = f'Your Cards are:' + str(p.hand)
                    await p.user.send(txt)
                return
    
    async def startGame():
        pass
                


    def getGameState(self, channel):
        for game in self.games:
            if game.channel == channel and game.status != GameStatus.ENDED:
                return game.status
        return GameStatus.NOT       
 


class Game:
    def __init__(self, host, channel):
        self.status = GameStatus.INIT
        #Guild
        self.channel = channel

        #Player
        self.hostUser = host
        self.playerList: Player = []

        #MessagesIDs 
        self.msg_initMsg = None
        self.dm_messages = []

        #GameStuff
        self.deck = Deck()
        self.pyramid = None


    def setStatus(self, newStatus):
        self.status = newStatus

    def playerJoin(self, player, emoji):
        self.playerList.append(Player(emoji,player,Hand()))

    def playerLeave(self, user):
        for p in self.playerList:
            if p == user:
                self.playerList.remove(p)
                return True
        return False
    
    def prepGame(self):
        self.deck.shuffleDeck()
        for player in self.playerList:
            player.hand = Hand(self.deck.drawCard(),self.deck.drawCard())
        self.pyramid = self.deck.drawPyramid()
        return self.playerList
        
            


    def __eq__(self, other):
        return self.channel == other.channel
    def isChannel(self, channel):
        return self.channel == channel

class Player:
    def __init__(self, emoji, user, hand):
        self.emoji = emoji
        self.user = user
        self.hand = hand

    def __eq__(self, o: object) -> bool:
        return o.user == self.user

class Hand:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
    def __str__(self):
        return '['+ self.left +']['+ self.right +']'



class GameStatus(Enum):
    NOT = 0
    INIT = 1
    LOGIN = 2
    PREP = 3
    RUNNING = 4
    ENDED = 5

import os
import discord
from enum import Enum

class Core:
    
    def __init__(self):
        self.games = []

    async def initGame(self, channel, host):
        self.games.append(Game(host,channel))
        
        txt = f'Willkommen bei BusBot. Jeder Mitspieler reagiert bitte mit einem Eigenen Emoji. Spieler {host.mention} das Spiel mit dem Emoji \U0001F504'
        m = await channel.send(txt)
        await m.add_reaction('\U0001F504') 
    
    async def joinGame(self, channel, player, emoji):
        game = next((game for game in self.games if game.isChannel(channel)), None)
        if game:
            game.playerJoin(player, emoji)

        print('Player:' +str(player)+ 'joind')

    async def startGame(self, user, channel):
        game = next((game for game in self.games if game.channel == channel), None)
        if not game or game.hostUser != user:
            return
        
        txt = f'Und los Geht es! Karten werden ausgeteilt! \n Wenn jeder seine Karten hat bitte \U0001F504 drücken. \n Mittspieler sind:\n'
        for player in game.playerList:
            txt = txt + f'{player[0]} => {player[1]}\n'
        m = await game.channel.send(txt)
        await m.add_reaction('\U0001F504') 
                


    def getGameState(self, channel):
        game = next((game for game in self.games if game.channel == channel), None)
 


class Game:
    def __init__(self, host, channel):
        self.status = GameStatus.INIT
        #Guild
        self.channel = channel

        #Player
        self.hostUser = host
        self.playerList = []

        #MessagesIDs 
        self.msg_initMsg = None
        self.dm_messages = []

    def playerJoin(self, player, emoji):
        self.playerList.append((emoji,player))

    def playerLeave(self, player):
        for p in self.playerList:
            if p[1] == player:
                self.playerList.remove(p)
                return True
        return False


    def __eq__(self, other):
        return self.channel == other.channel
    def isChannel(self, channel):
        return self.channel == channel


    



class GameStatus(Enum):
    NOT = 0
    INIT = 1
    LOGIN = 2
    RUNNING = 3
    ENDED = 4



class Game:

    def __init__(self, guild, host):
        #Guild
        self.guild = guild

        #Player
        self.hostUser = host
        self.playerList = []

        #MessagesIDs 
        self.msg_initMsg = None
        self.dm_messages = []

    



class GameStatus(Enum):
    INIT = 0
    LOGIN = 1


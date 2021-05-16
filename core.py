import os
import discord
from enum import Enum

class Core:
    
    def __init__(self):
        self.games = []

    async def initGame(self, channel, guild, host):
        self.games.append(Game(guild,host,channel))
        
        txt = f'Willkommen bei BusBot. Jeder Mitspieler reagiert bitte mit einem Eigenen Emoji. Spieler {host.mention} das Spiel mit dem Emoji \U0001F504'
        m = await channel.send(txt)
        await m.add_reaction('\U0001F504') 
    
    async def joinGame(self, guild, player, emoji):
        for game in self.games:
            if game.guild == guild:
                game.playerJoin(player, emoji)

    async def startGame(self, user, guild):
        game = next((game for game in self.games if game.guild == guild), None)
        if game != None:
            if game.hostUser != user:
                return
        
        txt = f'Und los Geht es! Karten werden ausgeteilt! \n Wenn jeder seine Karten hat bitte \U0001F504 drücken. \n Mittspieler sind:\n'
        for player in game.playerList:
            txt = txt + f'{player[0]} => {player[1]}\n'

        m = await game.channel.send(txt)
        await m.add_reaction('\U0001F504') 
                


    def getGameState(self, guild):
        return next((game.status for game in self.games if game.guild == guild), [GameStatus.NOT])
        
                
        


class Game:
    def __init__(self, guild, host, channel):
        self.status = GameStatus.INIT
        #Guild
        self.guild = guild
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


    



class GameStatus(Enum):
    NOT = 0
    INIT = 1
    LOGIN = 2


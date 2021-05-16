import os
import discord
from enum import Enum

class Core:
    
    def __init__(self):
        self.games = []

    async def initGame(self, channel, guild, host):
        self.games.append(Game(guild,host))
        await channel.send('Hi')
        


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


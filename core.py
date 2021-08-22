import os
import discord
from enum import Enum

from discord.message import Message
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
        game = self.getGame(channel)
        if game.channel == channel and game.status != GameStatus.ENDED and game.hostUser == user:
            game.setStatus(GameStatus.PREP)
            txt = f'Und los Geht es! Karten werden ausgeteilt! \n Wenn jeder seine Karten hat bitte \U0001F504 drücken. \n Mittspieler sind:\n'
            for player in game.playerList:
                txt = txt + f'{player.emoji} => {player.user}\n'
            msg = await game.channel.send(txt)
            await msg.add_reaction('\U0001F504')
            for player in game.prepGame():
                txt = f'Your Cards are:' + str(player.hand)
                dm_msg = await player.user.send(txt)
                game.add_DMmsg(user, dm_msg)                
        else:
            pass
            #TODO: If should not be wrong
               
    
    async def rdyGame(self, channel, user):
        game = self.getGame(channel)
        await game.del_DMmsg(user).delete()    
        if game.check_gameStart():
            game.setStatus(GameStatus.RUNNING)
            #TODO Pyramid start
            await self.round(channel)

    async def round(self, channel):
        game = self.getGame(channel)
        
        txt = f"Das ist die pyramide\n'''" + game.ppyramid() + "'''"
        msg = await game.channel.send(txt)
        
                


    def getGameState(self, channel):
        for game in self.games:
            if game.channel == channel and game.status != GameStatus.ENDED:
                return game.status
        return GameStatus.NOT
    
    def getGame(self, channel):
        return next((game for game in self.games if game.isChannel(channel)), None)
 


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
        self.round = 0


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
    
    def add_DMmsg(self, user, msg):
        self.dm_messages.append((user, msg))

    def del_DMmsg(self, user) -> Message:
        for dmmsg in self.dm_messages:
            if dmmsg[0] == user:
                self.dm_messages.remove(dmmsg)
                return dmmsg[1]
                
    
    def check_gameStart(self):
        return len(self.dm_messages) == 0


    
    def __eq__(self, other):
        return self.channel == other.channel
    def isChannel(self, channel):
        return self.channel == channel

    def card(self):
        return self.pyramid[round-1]

    def printPyramid(self, anzahl=10):
        p = self.pyramid
        c = 9
        while 10-anzahl != c:
            p[anzahl] = 'XX'
            c = c - 1
        out = "*********************************\n"\
            "***             "+p[9]+"            ***\n"\
            "***          "+p[8]+"    "+p[7]+"         ***\n"\
            "***       "+p[6]+"    "+p[5]+"    "+p[4]+"      ***\n"\
            "***    "+p[3]+"    "+p[2]+"    "+p[1]+"    "+p[0]+"   ***"
        return out

    def ppyramid(self):
        p = ['XX','XX','XX','XX','XX','XX','XX','XX','XX','XX']
        for i in range(0,self.round):
            p[i] = self.pyramid[i]
        return  ""+p[9]+" \n"+p[8]+" "+p[7]+" \n"+p[6]+" "+p[5]+" "+p[4]+" \n"+p[3]+" "+p[2]+" "+p[1]+" "+p[0]
    
        


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
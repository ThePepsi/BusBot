import os
import discord
from enum import Enum

from discord.message import Message
from mGameCore.Deck import Deck

class Core:
    
    def __init__(self):
        self.games = []

        self.emojis = {
            'next':      '\U0001F504',
            'left_card': '\U0001F448',
            'right_card':'\U0001F449',
        }

    async def initGame(self, channel, host):
        game = Game(host,channel)
        self.games.append(game)
        
        txt = f'Willkommen bei BusBot. Jeder Mitspieler reagiert bitte mit einem Eigenen Emoji. Spieler {host.mention} das Spiel mit dem Emoji \U0001F504'
        m = await channel.send(txt)
        await m.add_reaction('\U0001F504')
         
        game.setStatus(GameStatus.LOGIN)
    
    async def joinGame(self, channel, user, emoji):
        game = next((game for game in self.games if game.isChannel(channel)), None)
        if game:
            game.playerJoin(user, emoji)

        print('Player: ' +str(user)+ ' joined')

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
            await self.round(channel, start=True)

    async def round(self, channel, start=False):
        game = self.getGame(channel)
        (card,pyramid) = game.pppyramid(start=start)
        txt = f"Die Neue Karte ist: [" + card + "]\nDas ist die Pyramide:" + pyramid + ""
        msg = await game.channel.send(txt)
        await msg.add_reaction('\U0001F504')
        await msg.add_reaction(self.emojis['left_card'])
        await msg.add_reaction(self.emojis['right_card'])
        

    async def over(self, channel):
        game = self.getGame(channel)
        
        txt = f"Game Over"
        msg = await game.channel.send(txt)

    async def p_has_card(self, user, channel, left=False, right=False):
        print('Here')
        game = self.getGame(channel)
        sips = game.check_to_sip(user, left, right)
        if sips and sips != 0:
            txt = f'{user.mention} : Darf {str(sips)} verteilen, bitte wähle einen Spieler zum Drinken.'
            msg = await channel.send(txt)
            for player in game.playerList:
                msg.add_reaction(player.emoji)
    
    async def give_sips(self, user, channel, emoji):
        game = self.getGame(channel=channel)
        (sips, getplayer) = game.give_sip(user, emoji)
        txt = f'{getplayer.mention} : Darf {str(sips)} TRINKEN, bedank dich bei {user}'


                


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
        if self.round == 10:
            return
        self.round = self.round + 1
        return self.pyramid[self.round-1]

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
        for i in range(0,self.round-1):
            p[i] = self.pyramid[i]
        return  "\n"+p[9]+" \n"+p[8]+" "+p[7]+" \n"+p[6]+" "+p[5]+" "+p[4]+" \n"+p[3]+" "+p[2]+" "+p[1]+" "+p[0]

    def pppyramid(self, start=False):
        p = ['XX','XX','XX','XX','XX','XX','XX','XX','XX','XX']
        if start:
            self.round = 0
            #p[0] = self.pyramid[0]
        
        for i in range(0,self.round+1):
            p[i] = self.pyramid[i]
        
        pyramid =  "\n"+p[9]+" \n"+p[8]+" "+p[7]+" \n"+p[6]+" "+p[5]+" "+p[4]+" \n"+p[3]+" "+p[2]+" "+p[1]+" "+p[0]
        card = self.pyramid[self.round] 
        self.round = self.round + 1
        if self.round == 10:
            self.status = GameStatus.OVER
        return (card, pyramid)
    
    def check_to_sip(self, user, left=False, right=False):
        # returns sipcount
        player = next((player for player in self.playerList if player.user.id == user.id), None)
        if not player:
            return
        card_number = self.pyramid[self.round-1][1]
        if left and player.hand.left[1] == card_number:
            player.has_sip = player.has_sip + (1 if self.round >= 9 else 0) + (1 if self.round >= 7 else 0) + (1 if self.round >= 4 else 0) + 1
        if right and player.hand.right[1] == card_number:
            player.has_sip = player.has_sip + (1 if self.round >= 9 else 0) + (1 if self.round >= 7 else 0) + (1 if self.round >= 4 else 0) + 1 

        return player.has_sip
    
    def give_sip(self, give_user, get_player_emoji):
        give_player = next((x for x in self.playerList if x.user.id == give_user.id), None)
        get_player = next((x for x in self.playerList if x.emoji == get_player_emoji), None)
        if not give_player or not get_player:
            raise TypeError
        sips = give_player.has_sip
        give_player.has_sip = 0
        get_player.drink_sip = get_player.drink_sip + sips
        return (sips, get_player.user)
                   
        
        



        

    
        


class Player:
    def __init__(self, emoji, user, hand):
        self.emoji = emoji
        self.user = user
        self.hand = hand

        self.has_sip = 0
        self.drink_sip = 0

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
    OVER = 5
    ENDED = 6
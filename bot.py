# bot.py
import os
import discord
from discord.abc import User
from discord.reaction import Reaction
from dotenv import load_dotenv


#Loading of Token from .env (request @ThePepsi)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

aktGameMsg = None
hostUser: discord.User = None
gameStatus = 'none'
playerList = []
deleteMsg = []

client = discord.Client()

@client.event
async def on_ready():
    #TODO Lern how to Guild. Meaning: Server should be deployeble on multible Discord Servers -> more people should play at the same time
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    #Test Print
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    
    
    @client.event
    async def on_message(message):
        #Dont answer on own messages
        if message.author == client.user:
            return

        print(f'Guild: {guild.name} User: {message.author} Message: {message.content}\n')

        if (message.content.startswith('.')):
            
            if(message.content.startswith('.initGame')):
                txt = f'Willkommen bei BusBot. Jeder Mitspieler reagiert bitte mit einem Eigenen Emoji. Spieler {message.author.mention} das Spiel mit dem Emoji \U0001F504'
                global aktGameMsg, gameStatus, hostUser
                aktGameMsg = await message.channel.send(txt)
                await aktGameMsg.add_reaction('\U0001F504')
                gameStatus = 'init'
                hostUser = message.author
                
                
        

    @client.event
    async def on_reaction_add(reaction, user):
        global aktGameMsg, gameStatus, playerList, hostUser, deleteMsg
        if(aktGameMsg == reaction.message and user != client.user and gameStatus == 'init' and user == hostUser and reaction.emoji == '\U0001F504'):
            print("start")

            txt = f'Und los Geht es! Karten werden ausgeteilt! \n Wenn jeder seine Karten hat bitte \U0001F504 drücken. \n Mittspieler sind:\n'
            for player in playerList:
                msg = await player[1].send("Hi Deine Karten Sind: Herz Sau und Blatt König, wenn du sie dir gemerkt hast, dann drücke bitte das \U0001F504 im Server")
                deleteMsg.append(msg)
                txt = txt + f'{player[0]} => {player[1]}'

            aktGameMsg = await reaction.message.channel.send(txt)
            await aktGameMsg.add_reaction('\U0001F504')
            gameStatus = 'wait4Ready'
            return

        if(aktGameMsg == reaction.message and user != client.user and gameStatus == 'init'):
            print(f'User: {reaction}=>{user} joind the Game.')
            print(user)
            print(client.get_user(user.id))
            
            playerList.append((reaction.emoji,user,user.id))
            return

        if(aktGameMsg == reaction.message and user != client.user and gameStatus == 'wait4Ready'):
            for x in reaction.message.reactions:
                if x.emoji == '\U0001F504':
                    count = x.count
                    break
            print(f'rdy: {user} ({count-1}/{len(deleteMsg)})')
            if(count-1 == len(deleteMsg)):
                for msg in deleteMsg:
                    await msg.delete()
                gameStatus = "running"
                txt = "Wuhu !!!!!!!!! Karten sind Gelöscht! Pyramide könnte jetzt gelegtwerden. Game kann losgehen! Und Pepsi ist Müde!"
                aktGameMsg = await reaction.message.channel.send(txt)

                
        

    @client.event
    async def on_reaction_remove(reaction, user):
        global aktGameMsg, gameStatus, playerList
        if(aktGameMsg == reaction.message and user != client.user and gameStatus == 'init'):
            print(f'User: {reaction}=>{user} leaved the Game.')
            playerList.remove(user)


client.run(TOKEN)
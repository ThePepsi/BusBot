# bot.py
import os
import discord
from core import Core, Game, GameStatus
from discord.abc import User
from discord.reaction import Reaction
from dotenv import load_dotenv

BOT_PREFIX = '.'

def main():
    #Loading of Token from .env (request @ThePepsi)
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client = discord.Client()
    core = Core()

    #events
    @client.event
    async def on_ready():
        print(f'{client.user} is online! Connected to:')
        print(' - ' + '\n - '.join([str(guild.name) for guild in client.guilds]))

    @client.event
    async def on_message(message):
        if message.guild:
            print(f'Guild: {message.guild.name} User: {message.author} Message: {message.content}\n')
        else:
            print(f'User: {message.author} Message: {message.content}\n')

        if message.content.startswith(BOT_PREFIX):
            msg = message.content[len(BOT_PREFIX):]

            if msg == 'initGame':
                #TODO: delete old running Game
                await core.initGame(channel=message.channel, host=message.author)

            core.getGameState(message.channel)

    @client.event
    async def on_reaction_add(reaction, user):
        if user.bot:
            return
        
        status: GameStatus = core.getGameState(reaction.message.channel) 

        if status == GameStatus.LOGIN and reaction.emoji == '\U0001F504':
            await core.prepGame(user, reaction.message.channel)
        if status == GameStatus.LOGIN and not reaction.emoji == '\U0001F504':
            #TODO: Dont let 2 people joint with same reaction
            #TODO: MULTIJOINABLE NOT GOOD
            #TODO: MaxPlayerCount
            await core.joinGame(reaction.message.channel, user, reaction)
        if status == GameStatus.PREP and reaction.emoji == '\U0001F504':
            await core.rdyGame(reaction.message.channel, user)
        if status == GameStatus.RUNNING and reaction.emoji == '\U0001F504':
            await core.round(reaction.message.channel)
        if status == GameStatus.OVER and reaction.emoji == '\U0001F504':
            await core.over(reaction.message.channel)
            


        

    client.run(TOKEN)

if __name__ == "__main__":
    # execute only if run as a script
    main()
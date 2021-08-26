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
        print('react')
        if user.bot:
            return
        
        status: GameStatus = core.getGameState(reaction.message.channel) 

        if status == GameStatus.LOGIN and reaction.emoji == core.emojis['next']:
            await core.prepGame(user, reaction.message.channel)
            return
        if status == GameStatus.LOGIN and not reaction.emoji == core.emojis['next']:
            #TODO: Dont let 2 people joint with same reaction
            #TODO: MULTIJOINABLE NOT GOOD
            #TODO: MaxPlayerCount
            await core.joinGame(reaction.message.channel, user, reaction)
            return
        if status == GameStatus.PREP and reaction.emoji == core.emojis['next']:
            await core.rdyGame(reaction.message.channel, user)
            return
        if status == GameStatus.RUNNING and reaction.emoji == core.emojis['next']:
            await core.round(reaction.message.channel)
            return
        if status == GameStatus.RUNNING and (reaction.emoji == core.emojis['left_card'] or reaction.emoji == core.emojis['right_card']):
            await core.p_has_card(user, reaction.message.channel, left=(True if reaction.emoji == core.emojis['left_card'] else False), right=(True if reaction.emoji == core.emojis['right_card'] else False))
            return
        if status == GameStatus.RUNNING:
            await core.give_sips(user, reaction.message.channel, reaction.emoji)
            pass
            return
        if status == GameStatus.OVER and reaction.emoji == core.emojis['next']:
            await core.over(reaction.message.channel)
            return
        print('ract2')
            


        

    client.run(TOKEN)

if __name__ == "__main__":
    # execute only if run as a script
    main()
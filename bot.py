# bot.py
import os
import discord
from core import Core
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
        print(f'Guild: {message.guild.name} User: {message.author} Message: {message.content}\n')

        if message.content.startswith(BOT_PREFIX):
            msg = message.content[len(BOT_PREFIX):]

            if msg == 'initGame':
                await core.initGame(channel=message.channel, guild=message.guild, host=message.author)

            


        

    client.run(TOKEN)

if __name__ == "__main__":
    # execute only if run as a script
    main()
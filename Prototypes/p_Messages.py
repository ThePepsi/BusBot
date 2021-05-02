# bot.py
import os
import discord
from dotenv import load_dotenv

#Loading of Token from .env (request @ThePepsi)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print('Server DEAD')


#Recive message
@client.event
async def on_message(message):
    #Dont answer on own messages
    if message.author == client.user:
        return

    print(message.content)

    if (message.content.startswith('.')):
        if message.content.startswith('.testMsg'):
            print('DM to :'+ str(message.author))
            txt = 'Test to send DM'

            await message.channel.send('This a Message in the Same Channel')
            await message.author.send('This is a DM Message')

client.run(TOKEN)

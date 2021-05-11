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

    #emoji = client.get_emoji(123456)
    
    if (message.content.startswith('.')):
        if message.content.startswith('.testMsg'):
            print('DM to :'+ str(message.author))
            await message.channel.send('This a Message in the Same Channel and not for Vu')
            #add an reaction to users Message
            #await message.add_reaction("✅")
            await message.add_reaction('\N{THUMBS UP SIGN}')
            await message.add_reaction('\N{Playing Card Black Joker}')
            
            #how to remove reactions
            await message.remove_reaction('\N{Playing Card Black Joker}')

            #clear all reactions
            await message.clear_reaction('\N{Playing Card Black Joker}')

            await message.author.send('This is a DM Message')
            await message.add_reaction('\N{THUMBS UP SIGN}')
            await message.add_reaction('\N{Playing Card Black Joker}')
           



client.run(TOKEN)

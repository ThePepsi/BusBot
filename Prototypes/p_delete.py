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

    print("READY DO DELETE SOME MESSAGES")

@client.event
async def on_message(message):
    if message.content.startswith(".deleteMsg"):
        await message.delete()
        print("Deleted Message")

client.run(TOKEN)
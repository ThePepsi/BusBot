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
    if message.content.startswith('.hello'):
        embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
        embedVar.add_field(name="Field1", value="hi", inline=False)
        embedVar.add_field(name="Field2", value="hi2", inline=False)
        await message.channel.send(embed=embedVar)


client.run(TOKEN)
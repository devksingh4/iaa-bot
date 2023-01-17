import discord
import os
from discord.ext import commands
from discord import Intents
import random
import requests

client = commands.AutoShardedBot(command_prefix=os.environ['PREFIX'],intents=Intents.all())

token = os.environ['DISCORD_TOKEN']

@client.event
async def on_ready():
  print('Logged in as: ' + str(client.user.name) + ' ' + str(client.user.id))
  activity = discord.Game(name=os.environ['ACTIVITY'])
  await client.change_presence(activity=activity)


@client.command()
async def ping(ctx):
  await ctx.send('Pong!')

@client.event
async def on_member_join(member):
    await client.send_message(member, """
Welcome to the IMSA Alumni Association Discord server. 
To get access to the server, please provide the first and last name you had at IMSA, and your Class Year.

For example, if John Doe graduated in 2003, send the following message:

`John Doe, 2003`

""")
    m = await client.wait_for_message(author=member, channel=member)
    ny = m.content.split(',')
    print(ny)
    if m.content == 'key':
        # give the user the role
        await client.send_message(member, 'Role added')
    else:
        await client.send_message(member, 'Incorrect key')

# refreshCache.start()
client.run(token)

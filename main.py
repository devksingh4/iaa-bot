import discord
import os
from discord.ext import commands
from discord import Intents
import pandas as pd

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



def verify_user(name, year):
  data = pd.read_csv("data.csv")
  df2 = data['Name'].str.contains(name, na=False, case=False)
  return df2.eq(True).all()

@client.event
async def on_member_join(member):
    await member.send("""
  Welcome to the IMSA Alumni Association Discord server. 
To get access to the server, please provide the first and last name you had at IMSA, and your Class Year.

For example, if John Doe graduated in 2003, send the following message:

`John Doe, 2003`

  """)
    m = await client.wait_for('message')
    ny = m.content.split(',')
    name = ""
    year = 0
    try:
      name = ny[0].strip()
      year = int(ny[1].strip())
    except:
      await member.send("You could not be verified. If you believe this is an error, please rejoin the server and try again. You will now be removed from the server. Goodbye!")
      await member.guild.kick(member)
      return

    if verify_user(name, year):
      await member.send("Welcome {}! You have been verified.".format(name))
    else:
      await member.send("You could not be verified. If you believe this is an error, please rejoin the server and try again. You will now be removed from the server. Goodbye!")
      await member.guild.kick(member)



client.run(token)

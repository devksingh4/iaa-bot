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
  data = pd.read_csv("./data/data.csv",  encoding='latin-1')
  data['OurName'] = (data['First Name'] + ' ' + data['Last Name']).str.lower()
  d = dict(zip(data['OurName'], data['Year']))
  try:
      return d[name.lower()] == int(year) 
  except KeyError:
      return False

def get_guild_mappings():
  return {
    "1989": "1061461730724675604",
    "1990": "1061464856924016652",
    "1991": "1061464856924016652",
    "1992": "1061464856924016652",
    "1993": "1061464856924016652",
    "1994": "1061464856924016652",
    "1995": "1061464926767562762",
    "1996": "1061464926767562762",
    "1997": "1061464926767562762",
    "1998": "1061464926767562762",
    "1999": "1061464926767562762",
    "2000": "1061464962427539497",
    "2001": "1061464962427539497",
    "2002": "1061464962427539497",
    "2003": "1061464962427539497",
    "2004": "1061464962427539497",
    "2005": "1061465099912630362",
    "2006": "1061465099912630362",
    "2007": "1061465099912630362",
    "2008": "1061465099912630362",
    "2009": "1061465099912630362",
    "2010": "1061465113703493664",
    "2011": "1061465113703493664",
    "2012": "1061465113703493664",
    "2013": "1061465113703493664",
    "2014": "1061465113703493664",
    "2015": "1061465119864918088",
    "2016": "1061465119864918088",
    "2017": "1061465119864918088",
    "2018": "1061465119864918088",
    "2019": "1061465119864918088",
    "2020": "1061465226278600745",
    "2021": "1061465226278600745",
    "2022": "1061465226278600745",
    "2023": "1061465226278600745",
    "2024": "1061465226278600745",
  }

def assign_roles(member, year):
  mappings = get_guild_mappings()
  member.add_roles([mappings[str(year)]], reason="Verified as IMSA Alum, Class of {}".format(str(year)))

@client.event
async def on_member_join(member):
    await member.send("""
  Welcome to the IMSA Alumni Association Discord server. 
To get access to the server, please provide the first and last name you had at IMSA, and your Class Year.

For example, if John Timothy Doe graduated in 2003, send the following message:

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
      await member.send("You could not be verified. If you believe this is an error, please rejoin the server and try again. Or, enter the same information in the verification channel and an admin will attempt to verify you manually. Goodbye!")
      return

    if verify_user(name, year):
      await member.send("Welcome {}! You have been verified.".format(name))
      assign_roles(member)
    else:
      await member.send("You could not be verified. If you believe this is an error, please rejoin the server and try again. Or, enter the same information in the verification channel and an admin will attempt to verify you manually. Goodbye!")
      return


client.run(token)
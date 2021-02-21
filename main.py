import os

import discord
import tweets
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents(messages=True, members=True, guilds=True, presences=True)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='rit ')

async def on_ready():
    print(f'{bot.user.name} is online!')

@bot.command(name='ping')
async def pingpong(ctx):
    response = 'pong'
    await ctx.send(response)

@bot.command(name='twitter')
async def get_tweet(ctx):
    tweet = tweets.get_new_tweet("RITTigers")
    await ctx.send(embed=tweet)



bot.run(TOKEN)
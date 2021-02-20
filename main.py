import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
import dining

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

@bot.command(name='dining', help="bcc - Brick City Café, cmc - Café & Market at Crossroads, tc - The Commons, gracies - Gracie's")
async def get_dining_menu(ctx, location):
    location, error, embeds = dining.get_menu(location)
    await ctx.send(location)
    if error:
        await ctx.send(error)
    else:
        for embed in embeds:
            await ctx.send(embed=embed)

bot.run(TOKEN)
import os

import discord
import tweets
from dotenv import load_dotenv
from discord.ext import commands, tasks
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

@bot.command(name='get_tweet')
async def get_tweet(ctx):
    tweet = tweets.get_new_tweet("RITTigers")
    try:
        await ctx.send(embed=tweet)
    except:
        await ctx.send(tweet)

@bot.command(name='dining', help="bcc - Brick City Café, cmc - Café & Market at Crossroads, tc - The Commons, gracies - Gracie's")
async def get_dining_menu(ctx, args):
    if args in ['bcc', 'cmc', 'tc', 'gracies']:
        location, error, embeds = dining.get_menu(args)
        await ctx.send(location)
        if error:
            await ctx.send(error)
        else:
            for embed in embeds:
                await ctx.send(embed=embed)
    elif args == 'hours-open': # get open places only
        embed = dining.get_hours(False)
        await ctx.send(embed=embed)
    elif args == 'hours':
        embed = dining.get_hours(True)
        await ctx.send(embed=embed)
    else:
        response = "Invalid command: rit dining <param>. See 'rit help dining' for more details."
        await ctx.send(response)


bot.run(TOKEN)
import os
import discord
import tweets
from dotenv import load_dotenv
from discord.ext import commands
import praw
from datetime import datetime
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


@bot.command(name='reddit_post')
async def grab_posts(ctx):
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    USER_AGENT = "RIT bot for hackathon"

    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                            client_secret=REDDIT_CLIENT_SECRET,
                            user_agent=USER_AGENT,
                            check_for_async=False)
    for submission in reddit.subreddit("rit").new(limit=1):
        if not submission.stickied:
            embed=discord.Embed(
            title=submission.title,
                url=submission.url,
                description=submission.selftext,
                color=discord.Color.blue())
            embed.set_footer(text= "by "+ str(submission.author) + " on " + datetime.utcfromtimestamp(int(submission.created_utc)).strftime('%Y-%m-%d %H:%M:%S'))
            await ctx.send(embed=embed)

            
@bot.command(name='twitter')
async def get_tweet(ctx):
    tweet = tweets.get_new_tweet("RITTigers")
    await ctx.send(embed=tweet)

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
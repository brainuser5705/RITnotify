import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import praw
from datetime import datetime

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


bot.run(TOKEN)
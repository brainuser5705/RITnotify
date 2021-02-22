import os
import tweepy
import time
import discord
from dotenv import load_dotenv
load_dotenv()

# Consumer Keys from developer portal
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')

# Have to get these from get_token.py
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Have to get these from get_token.py


# Twitter login and authentication
callback_uri = "oob" # url
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, callback_uri)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def get_tweets(user, num_tweets = 1):
    getuser = api.get_user(user)
    user_tl = api.user_timeline(screen_name = getuser.screen_name,
                                count = num_tweets,
                                include_rts = False,
                                tweet_mode = 'extended')
    i = 0
    string = ""
    for info in user_tl:   # Need some help trying to get data off of user_tl without doing for loop
        i = i + 1
        string += "\nTweet #" + str(i) + "\nTweet ID " + str(info.id) + "\nCreated " + str(info.created_at) + "\nContents: \n" + info.full_text

    return string

def get_new_tweet(user):
    getuser = api.get_user(user)
    user_tl = api.user_timeline(screen_name = getuser.screen_name,
                                count = 1,
                                include_rts = False,
                                tweet_mode = 'extended')
    
    for info in user_tl:
        tweet_id = str(info.id) # Getting the most recent tweet ID, might need to refactor
                                # to not include the for loop

    print("@" + getuser.screen_name + "'s newest tweet:") # We found the tweet
    
    for info in user_tl:                        # Might need some help
        embed = discord.Embed( 
                title="@" + getuser.screen_name + " has posted a new tweet",
                url="https://twitter.com/@RITTigers",
                description=info.full_text,
                color=discord.Color.orange())                
        embed.set_footer(text="Posted at " + str(info.created_at))
    return embed

#get_tweets("ritTigers")
#get_new_tweet("ritTigers")
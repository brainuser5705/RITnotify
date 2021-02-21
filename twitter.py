import tweepy
import webbrowser
import time

consumer_key = "wQqQ0anvvoJc6Kxn9rtCKnto2"
consumer_secret = "10IXsG9AETGvEv1vf7KfQfWHcx8ra8GhtS3MR5tIwiKMKDQ46T"
access_token = "595909509-KwLgiGuHan8ATKSfjxVVAUhP2iOJLUo0NyNDuHMQ"
access_token_secret = "Vz8vfhljPjAcR6W7ECo0IH6sqB1GYv7WWIdLFF92D20CA"
callback_uri = "oob" # url

auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
public_tweets = api.home_timeline()

for tweet in public_tweets:
    print(tweet.text)





#redirect_url = auth.get_authorization_url()
#webbrowser.open(redirect_url)
#user_pin_input = input("Whats the pin value: ")
#auth.get_access_token(user_pin_input)
#print(auth.access_token, auth.access_token_secret)
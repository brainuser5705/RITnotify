import tweepy
import webbrowser
import time

# Consumer Keys from Twitter developer portal
consumer_key = input("Enter consumer API key: ")
consumer_secret = input("Enter consumer API key secret: ")

# Twitter login
callback_uri = "oob" # url
auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
api = tweepy.API(auth)

# Opens web page for authentication
redirect_url = auth.get_authorization_url()
webbrowser.open(redirect_url)


user_pin_input = input("Enter the 7-digit PIN code to reveal the access tokens: ")
# Gets the access keys
auth.get_access_token(user_pin_input)
print("Access Token: " + auth.access_token)
print("Access Token Secret: " + auth.access_token_secret)
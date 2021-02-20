import tweepy
import webbrowser
import time

# Consumer Keys from developer portal
consumer_key = ""
consumer_secret = ""

# Have to get these from get_token.py
access_token = ""
access_token_secret = ""

# Twitter login and authentication
callback_uri = "oob" # url
auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def get_tweets(user, num_tweets = 1):
    getuser = api.get_user(user)
    user_tl = api.user_timeline(screen_name = getuser.screen_name,
                                count = num_tweets,
                                include_rts = False,
                                tweet_mode = 'extended')
    i = 0
    for info in user_tl:
        i = i + 1
        print("Tweet #" + str(i))
        print("Tweet ID " + str(info.id))
        print("Created " + str(info.created_at))
        print("Contents: \n" + info.full_text)
    
    return str(info.id)

def get_status(info_id, user):
    i = 0
    with open("recent_tweet.txt", "r+") as file:
        for line in file:
            for id_num in info_id:
                if line[i] != id_num: # If there is a mismatch on the characters

                    print("Found new tweet!") # We found the tweet
                    new_info_id = get_tweets(user, 1) # Get the tweet
                    file.seek(0) # Go to the beginning of the text file
                    file.truncate() # Remove the contents of the text file
                    file.write(new_info_id) # Write the new info id
                    file.close()
                    return new_info_id # return the new tweet id
                print("No new tweet found.")
                return None


get_status(get_tweets("ritTigers"), "ritTigers")

#redirect_url = auth.get_authorization_url()
#webbrowser.open(redirect_url)
#user_pin_input = input("Whats the pin value: ")
#auth.get_access_token(user_pin_input)
#print(auth.access_token, auth.access_token_secret)
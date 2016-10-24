import random
import json
import os
import time
import tweepy
import configargparse
import gzip
from datetime import datetime

# connect to twitter API and tweet
# from: https://videlais.com/2015/03/02/how-to-create-a-basic-twitterbot-in-python/
class TwitterAPI:
    def __init__(self, cfg):
        auth = tweepy.OAuthHandler(cfg["consumer_key"], cfg["consumer_secret"] )
        auth.set_access_token(cfg["access_token"], cfg["access_token_secret"])
        self.api = tweepy.API(auth)

    def tweet(self, message):
        self.api.update_status(status=message)

# get a charity record from the file prepared by `fetch_charity_data.py`
# returns a formatted tweet
def get_charity_tweet(filename):

    with gzip.open(filename, "r") as c:
        chars = json.load(c)
        regno = random.choice(list(chars.keys()))
        char = chars[regno]

        # correct common misformed URL in websites
        # @todo - make this a bit more robust
        if char["website"][0:4]!="http":
            char["website"] = "http://" + char["website"]
        
        # return the tweet format
        return "{name} [{regno}] {website}".format(name=char["title"], regno=regno, website=char["website"])

if __name__ == "__main__":
    
    p = configargparse.ArgParser(ignore_unknown_config_file_keys=True)
    p.add('-c', '--my-config', required=True, default="example.cfg", is_config_file=True, help='config file path')
    
    # Twitter connection details
    p.add('--consumer-key', help='Twitter authorisation: consumer key')
    p.add('--consumer-secret', help='Twitter authorisation: consumer secret')
    p.add('--access-token', help='Twitter authorisation: access token')
    p.add('--access-token-secret', help='Twitter authorisation: access token secret')
    
    # Time to sleep between tweets (in seconds - default is one hour)
    p.add('-s', '--sleep', default=3600, type=int, help='Time to sleep between tweets (in seconds - default is one hour)')
    
    # filename of charity data file
    p.add("-f", "--data-file", default="charity_names.json.gz", help="Location of charity data file")

    is_heroku = os.environ.get('IS_HEROKU', None)
    if is_heroku:
        options = p.parse_args([
            '--consumer-key', os.environ.get('CONSUMER_KEY'),
            '--consumer-secret', os.environ.get('CONSUMER_SECRET'),
            '--access-token', os.environ.get('ACCESS_TOKEN'),
            '--access-token-secret', os.environ.get('ACCESS_TOKEN_SECRET'),
            '--sleep', os.environ.get('SLEEP'),
            '-c', None,
        ])
    else:
        options = p.parse_args()
    
    # connect to Twitter API
    twitter = TwitterAPI(vars(options))
    print("Connected to twitter. User: [{}]".format( twitter.api.me().screen_name ) )
    print("Tweeting every {} seconds".format( options.sleep ))
    
    while True:
        tweet = get_charity_tweet( options.data_file )
        twitter.tweet(tweet)
        print("{:%Y-%m-%d %H:%M:%S}: {tweet}".format(datetime.now(), tweet=tweet) )
        time.sleep(options.sleep)



from __future__ import print_function
import time
from datetime import datetime
import tweepy
import configargparse
import gzip
import requests

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
def get_charity_tweet(url):

    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        char_data = r.json()
        char = {
            "title": char_data["known_as"]
        }

        if char_data.get("ccew_number"):
            regno = char_data["ccew_number"]
            char["website"] = 'http://beta.charitycommission.gov.uk/charity-details/?regid={}&subid=0'.format(regno)
            char["title"] = char["title"]
        elif char_data.get("ccni_number"):
            regno = "NIC{}".format(char_data["ccni_number"].replace("NIC", ""))
            char["website"] = char_data["ccni_link"]
        elif char_data.get("oscr_number"):
            regno = char_data["oscr_number"]
            char["website"] = char_data["oscr_link"]


        if char_data["url"] and char_data["url"] != "":
            char["website"] = char_data["url"]

        # correct common misformed URL in websites
        # @todo - make this a bit more robust
        if char["website"][0:4]!="http":
            char["website"] = "http://" + char["website"]

        # return the tweet format
        return "{name} [{regno}] {website}".format(name=char["title"], regno=regno, website=char["website"])

if __name__ == "__main__":

    p = configargparse.ArgParser(ignore_unknown_config_file_keys=True)
    p.add('-c', '--my-config', default="example.cfg", is_config_file=True, help='config file path')

    # Twitter connection details
    p.add('--consumer-key', help='Twitter authorisation: consumer key')
    p.add('--consumer-secret', help='Twitter authorisation: consumer secret')
    p.add('--access-token', help='Twitter authorisation: access token')
    p.add('--access-token-secret', help='Twitter authorisation: access token secret')

    # Time to sleep between tweets (in seconds - default is one hour)
    p.add('-s', '--sleep', default=3600, type=int, help='Time to sleep between tweets (in seconds - default is one hour)')

    # filename of charity data file
    p.add("-u", "--url", default="http://localhost:8080/random.json?active", help="Location of charity data url")

    p.add("--debug", action='store_true', help="Debug mode (doesn't actually tweet)")

    options = p.parse_args()

    # connect to Twitter API
    twitter = TwitterAPI(vars(options))
    print("Connected to twitter. User: [{}]".format(twitter.api.me().screen_name))
    print("Tweeting every {} seconds".format(options.sleep))

    while True:
        try:
            tweet = get_charity_tweet(options.url)
        except:
            continue
        if not options.debug:
            try:
                twitter.tweet(tweet)
            except tweepy.error.TweepError:
                continue
        print("{:%Y-%m-%d %H:%M:%S}: {tweet}".format(datetime.now(), tweet=tweet))
        time.sleep(options.sleep)

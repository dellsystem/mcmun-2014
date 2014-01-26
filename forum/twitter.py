import codecs
import sys

import tweepy
import twilio
from twilio.rest import TwilioRestClient

import config


auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_key, config.access_secret)
api = tweepy.API(auth)

client = TwilioRestClient(config.account_sid, config.auth_token)

current_id = 1

def send_sms(message):
    client.sms.messages.create(to=config.to_number, from_=config.from_number,
        body=message)


class ForumStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        global current_id
        tweet = status.text
        print tweet
        message = "%d: %s" % (current_id, tweet)
        send_sms(message)

        # Save it to disk
        # Should really be using Redis or something but not enough time lol
        tweet_file = codecs.open('data/%d' % current_id, 'w', encoding='utf-8')
        tweet_file.write(tweet)

        current_id += 1

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream


stream_api = tweepy.streaming.Stream(auth, ForumStreamListener())
stream_api.filter(track=['mcmunforum'])

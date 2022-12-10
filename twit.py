

import math
import os
import textwrap
import tweepy


from tweepy import OAuthHandler
from chatgpt import ChatGPT
from dotenv import load_dotenv

from utils import *

load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")


auth = OAuthHandler(API_KEY, SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = "last_seen_id.txt"
THREAD_FILE_NAME = "last_keyword_id.txt"


class TwitterApp(ChatGPT):

    def searchMention(self):
        last_seen_id = retreive_last_id(FILE_NAME)
        mentions = api.mentions_timeline(count=5, since_id=last_seen_id)
        for mention in reversed(mentions):
            if mention.in_reply_to_status_id_str is None and "@kcibdev" in mention.text.lower():
                text = trimText(mention.text)
                # print(text)
                chat_msg = self.sendMessage(text)
                self.shorten_text(
                    f"@{mention.user.screen_name}", chat_msg, mention.id)
                #chat_msg = "Hello " + text
                # print(chat_msg)
                # if chat_msg is not None:
                #     self.updateReply(chat_msg, mention)
                last_seen_id = mention.id
                store_last_id(last_seen_id, FILE_NAME)

    def updateReply(self, message, mentionId):
        return api.update_status(
            message, in_reply_to_status_id=mentionId, auto_populate_reply_metadata=True)

    def shorten_text(self, tweet, mentionId):

        # obtain length of tweet, which is 1471 characters
        tweet_length = len(tweet)

        # check length
        if tweet_length <= 275:
            new_tweet = replace_words_in_tweet(tweet)
            self.updateReply(f'{new_tweet}', mentionId)
            print(tweet)
            # do some here

        elif tweet_length >= 280:

            # divided tweet_length / 280
            # You might consider adjusting this down
            # depending on how you want to format the
            # tweet.
            tweet_length_limit = tweet_length / 280

            # determine the number of tweets
            # math.ceil is used because we need to round up
            tweet_chunk_length = tweet_length / \
                math.ceil(tweet_length_limit)

            # chunk the tweet into individual pieces
            tweet_chunks = textwrap.wrap(tweet,  math.ceil(
                tweet_chunk_length), break_long_words=False)

            last_update_id = None
            for x, chunk in zip(range(len(tweet_chunks)), tweet_chunks):
                new_chunk = replace_words_in_tweet(chunk)
                updatedData = self.updateReply(
                    f'''{new_chunk}''', last_update_id)
                print(updatedData.id)
                last_update_id = updatedData.id

    def send_tweet_thread(self):
        last_id = retreive_last_id(THREAD_FILE_NAME)

        try:
            if tweets_thread_list[last_id + 1] is not None and last_id < tweets_thread_list[last_id + 1]['id']:
                thread_question = tweets_thread_list[last_id + 1]['keyword']
                gpt_responds = self.sendMessage(thread_question)
                if gpt_responds is not None:
                    self.shorten_text(gpt_responds, None)
                    store_last_id(last_id + 1, THREAD_FILE_NAME)
                    # updateData = self.updateReply(gpt_responds, last_update_id)
                    # print(updateData.id)
                    # last_update_id = updateData.id

        except IndexError as err:
            print(err)
            print(err.args)

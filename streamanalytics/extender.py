import tweepy as tw
import os
import json
import time
import logging
import random

class Extender():
    def __init__(self, credentials):
        auth = self.oauther(credentials[0], credentials[1],
                            credentials[2], credentials[3])
        self.api = tw.API(auth)
        logging.debug("Initiated object of class Extender")

    def __call__(self, input_fname, output_fname, num_tweets=100,
                    wait_per_request=0):
        """Takes name of a file containing tweets, fetches full version of these
        tweets and then saves these into an output file

        Keyword arguments:
        input_fname -- (string) the file to read tweets from
        output_fname -- (string) the file to write extended tweets to
        num_tweets -- (int) number of tweets to fetch per request
        wait_per_request -- (int) number of seconds to wait before requesting
        """
        rlstatus = self.rate_limit_status('resources', 'statuses',
                                            '/statuses/lookup')
        remaining = rlstatus['remaining']
        limit = rlstatus['limit']
        reset = rlstatus['reset']

        logging.info("Remaining tweets: %s/%s, Reset at: %s", remaining, limit,
                     reset)

        cnt = 0
        tw_cnt = 0
        tweets = self.read_tweet_ids(input_fname, num_tweets=num_tweets)
        for tweets_set in tweets:
            cnt += 1

            len_tw_set = len(tweets_set)
            if len_tw_set == 0:
                break
            tw_cnt += len_tw_set

            now = time.time()
            if (now > reset) or (random.random() < 0.1):
                logging.info("Updating rate limit status")
                time.sleep(1)
                rlstatus = self.rate_limit_status('resources', 'statuses',
                                                    '/statuses/lookup')
                logging.info("Updated rate limit status %s", rlstatus)
                remaining = rlstatus['remaining']
                limit = rlstatus['limit']
                reset = rlstatus['reset']

                cnt = 1

            # if too many requests are sent then wait till rate limit is reset
            if cnt > limit:
                now = time.time()
                logging.warning("Rate limit is reached. Waiting till reset. " +
                                "%s seconds", reset-now+10)
                if reset > now:
                    time.sleep(reset-now+10)
                cnt = 1

            tweet_ids = self.extract_tweet_ids(tweets_set)
            extended_tweets = self.extend_tweets(tweet_ids)
            full_tweets = self.fill_missing_tweets(extended_tweets, tweets_set)
            self.save_tweets(full_tweets, output_fname)

            logging.info("Updated %s tweets till now", tw_cnt)
            time.sleep(wait_per_request)

        logging.info("Done extending tweets")

    def read_tweet_ids(self, fname, num_tweets=float('Inf')):
        """Reads a certain number of lines with each call from file

        Keyword arguments:
        fname -- (string) the file to read
        num_tweets -- (int) number of lines to read with one call

        Returns:
        tweets -- (generator of json objects) a list that contains tweets
        """
        tweets = []
        with open(fname) as f:
            for line in f:
                data_row = json.loads(line)
                tweets.append(data_row)
                if (len(tweets)>=num_tweets):
                    yield tweets
                    tweets = []
            yield tweets

    def extract_tweet_ids(self, tweets):
        tweet_ids = []
        for tweet in tweets:
            tweet_ids.append(tweet['tweet_id'])
        return tweet_ids

    def extend_tweets(self, tweet_ids):
        tweets = self.api.statuses_lookup(id_=tweet_ids,
                                          tweet_mode = 'extended')
        filtered_tweets = []
        for status in tweets:
            text = status.full_text
            user_id = status.user.id
            date_time = status.created_at.strftime('%m/%d/%Y %H:%M:%S')
            tweet_id = status.id
            tweet = {
                'user_id': user_id,
                'date_time':date_time,
                'tweet_content': text,
                'tweet_id': tweet_id
                }
            filtered_tweets.append(tweet)

        return filtered_tweets

    def fill_missing_tweets(self, e_tweets, o_tweets):
        """If extended tweets have certain tweets missing then fetch those
        tweets from original tweets

        Keyword arguments:
        e_tweets -- (list of json objects) extended tweets with missing ones
        o_tweets -- (list of json objects) original tweets without missing ones

        Returns:
        e_tweets -- (list of json objects) extended tweets without missing ones
        """
        o_tweet_ids = self.extract_tweet_ids(o_tweets)
        e_tweet_ids = self.extract_tweet_ids(e_tweets)

        missing_tweet_ids = list(set(o_tweet_ids) - set(e_tweet_ids))
        all_tweets = e_tweets
        for missing_tweet_id in missing_tweet_ids:
            for o_tweet in o_tweets:
                if missing_tweet_id == o_tweet['tweet_id']:
                    all_tweets.append(o_tweet)

        return all_tweets


    def save_tweets(self, tweets, fname):
        with open(fname, 'a') as f:
            for tweet in tweets:
                f.write(str(json.dumps(tweet, ensure_ascii=False)))
                f.write(os.linesep)

    def oauther(self, consumer_key, consumer_secret,
                    access_token, access_token_secret):
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth

    def rate_limit_status(self, *args):
        rlstatus = self.api.rate_limit_status()
        for arg in args:
            rlstatus = rlstatus[arg]

        logging.info("Fetched rate limit status. %s", rlstatus)
        return rlstatus

def main():
    # an example of how to run the class defined above
    pass


if __name__ == '__main__':
    main()

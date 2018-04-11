import tweepy as tw
import os
import json

class LocalStreamListener(tw.StreamListener):

    def on_status(self, status):
        self.save_status(status)

    def on_error(self, status_code):
        print(status_code)

    def save_status(self, status):
        path_str = os.path.join( os.getcwd(), 'data' )
        if not os.path.exists(path_str):
            os.makedirs(path_str)
        fname = os.path.join(path_str, 'data.txt')

        with open(fname,'a') as f:
            text = status.text
            user_id = status.user.id
            date_time = status.created_at.strftime('%m/%d/%Y %H:%M:%S')
            tweet_id = status.id
            json_obj = json.dumps({
                'user_id': user_id,
                'date_time':date_time,
                'tweet_content': text,
                'tweet_id': tweet_id
                }, ensure_ascii=False)
            f.write(json_obj + os.linesep)

class Streamer():
    def __init__(self):
        self.streamlistener = LocalStreamListener()

    def __call__(self, credentials, tags):
        auth = self.oauther(credentials[0], credentials[1],
                            credentials[2], credentials[3])
        api = tw.API(auth)
        self.stream = tw.Stream(auth = api.auth, listener=self.streamlistener)
        self.stream.filter(track=tags, async=True)

    def disconnect(self):
        self.stream.disconnect()

    def oauther(self, consumer_key, consumer_secret,
                    access_token, access_token_secret):
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        return auth

def main():
    # an example of how to run the class defined above
    streamer = Streamer()

    credentials = ['<consumer_token>',
                '<consumer_secret>',
                '<access_token>',
                '<access_token_secret>']
    tags = ['#QGvsIU',
            '#IUvsQG',
            '#QuettaGladiators',
            '#IslamabadUnited',
            '#PSL2018',
            '#PSL',
            '#PSL18']

    streamer(credentials, tags)


if __name__ == '__main__':
    main()

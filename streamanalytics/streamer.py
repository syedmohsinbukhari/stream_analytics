import tweepy as tw
import os

class LocalStreamListener(tw.StreamListener):

    def on_status(self, status):
        # tweet_date_time = status.created_at.strftime('%m/%d/%Y %H:%M:%S')
        self.save_status(status)

    def on_error(self, status_code):
        print(status_code)

    def save_status(self, status):
        path_str = os.path.join( os.getcwd(), 'data' )
        fname = os.path.join(path_str, 'data.txt')

        with open(fname,'a') as f:
            text = status.text
            user_id = status.user.id
            date_time = status.created_at.strftime('%m/%d/%Y %H:%M:%S')
            f.write(str({
                'user_id': user_id,
                'date_time':date_time,
                'tweet_content': text
                }) + '\n')

class Streamer():
    def __call__(self, credentials, tags):
        streamlistener = LocalStreamListener()
        api = self.oauther(credentials[0], credentials[1],
                            credentials[2], credentials[3])
        stream = tw.Stream(auth = api.auth, listener=streamlistener)
        stream.filter(track=tags, async=True)

    def oauther(self, consumer_key, consumer_secret,
                    access_token, access_token_secret):
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tw.API(auth)

        return api

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

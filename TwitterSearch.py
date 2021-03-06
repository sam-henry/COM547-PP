from tweepy import OAuthHandler
import tweepy
import MySQLdb
import time


#        replace mysql.server with "localhost" if you are running via your own server!
#                        server       MySQL username	MySQL pass  Database name.
conn = MySQLdb.connect("localhost","root","","premierpredict",use_unicode=True, charset='utf8')

# consumer key, consumer secret, access token, access secret.
ckey = ""
csecret = ""
atoken = ""
asecret = ""

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)


count = 49
team = 'NUFC'
gw = 39
query = '#%s' % team


for tweet in limit_handled(tweepy.Cursor(api.search, q=query, lang='en', tweet_mode='extended', since='2018-05-03',
                                         until='2018-05-09').items()):
        if not tweet.retweeted and 'RT @' not in tweet.full_text:
            print(tweet.full_text, tweet.created_at)
            tweetdb=tweet.full_text
            tweetdatedb=tweet.created_at
            count += 1
            c = conn.cursor()
            c.execute("INSERT INTO tweetdata (tweet, date, team, gameweek) VALUES (%s,%s,%s,%s)",
                      (tweetdb, tweetdatedb, team, gw))

            conn.commit()
        if count >= 60:
            break

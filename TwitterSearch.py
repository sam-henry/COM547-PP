from tweepy import OAuthHandler
import tweepy
import MySQLdb
import time


#        replace mysql.server with "localhost" if you are running via your own server!
#                        server       MySQL username	MySQL pass  Database name.
conn = MySQLdb.connect("localhost","root","","premierpredict",use_unicode=True, charset='utf8')

# consumer key, consumer secret, access token, access secret.
ckey = "UJ5LUyq9RZ8dAUiwRvKtHgOWi"
csecret = "oUc85NGKuIqTenTtyLkkOf40e1ohcXoUVx4gyQEG9giMhZfdoi"
atoken = "526890392-8WQJBhoB53f69mtnIjaPYCAaLBlYrtCXxUAqGTXc"
asecret = "utmPGRtezzrUvzP6qzTBLYstqy5cYP0XDMNEGH5UqEn8k"

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)

count = 0
team = 'SCFC'
gw = 30
query = '#%s' % team


for tweet in limit_handled(tweepy.Cursor(api.search, q=query, lang='en', tweet_mode='extended', since='2018-04-11',
                                         until='2018-04-15').items()):
        if not tweet.retweeted and 'RT @' not in tweet.full_text:
            print(tweet.full_text, tweet.created_at)
            tweetdb=tweet.full_text
            tweetdatedb=tweet.created_at
            count += 1
            c = conn.cursor()
            c.execute("INSERT INTO tweetdata (tweet, date, team, gameweek) VALUES (%s,%s,%s,%s)",
                      (tweetdb, tweetdatedb, team, gw))

            conn.commit()
        if count >= 110:
            break

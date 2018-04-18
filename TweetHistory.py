import requests
from requests_oauthlib import OAuth1Session
import MySQLdb
import json

#        replace mysql.server with "localhost" if you are running via your own server!
#                        server       MySQL username	MySQL pass  Database name.
conn = MySQLdb.connect("localhost","root","","premierpredict",use_unicode=True, charset='utf8')

# consumer key, consumer secret, access token, access secret.
ckey = "UJ5LUyq9RZ8dAUiwRvKtHgOWi"
csecret = "oUc85NGKuIqTenTtyLkkOf40e1ohcXoUVx4gyQEG9giMhZfdoi"
atoken = "526890392-8WQJBhoB53f69mtnIjaPYCAaLBlYrtCXxUAqGTXc"
asecret = "utmPGRtezzrUvzP6qzTBLYstqy5cYP0XDMNEGH5UqEn8k"


twitter = OAuth1Session(ckey,
                        client_secret=csecret,
                        resource_owner_key=atoken,
                        resource_owner_secret=asecret)
# , "next": ""

gw = 33
team = 'WHU'
next = 'eyJhdXRoZW50aWNpdHkiOiJmNWM4NDg1ODBjZGZmNWU3MDcyY2MyMTJmMmY0MTA1MDcwMTI0ZWJlYTdmZWQ1ZDE0ZDNhNDY2OWI5ZTNiMDBkIiwiZnJvbURhdGUiOiIyMDE4MDMxOTEyMDAiLCJ0b0RhdGUiOiIyMDE4MDQwNzEwMzAiLCJuZXh0IjoiMjAxODA0MDQyMDM4MTItOTgxNjMyMDQ4MjIwNzg2Njg3LTAifQ=='

url = 'https://api.twitter.com/1.1/tweets/search/30Day/PP30Days.json'
query = '{"query": "#%s", "fromDate": "201803191200", "toDate": "201804071030"}' % team
# query = '{"query": "#%s", "fromDate": "201803191200", "toDate": "201804071030", "next": "%s"}' % (team, next)
count = 68
myResponse = twitter.post(url, query).json()
print(myResponse)
tweets = myResponse["results"]
for tweet in tweets:
    if not tweet["retweeted"] and 'RT @' not in tweet["text"] and tweet["lang"] == "en":
        print(tweet["text"], tweet["created_at"])
        tweetdb=tweet["text"]
        tweetdatedb=tweet["created_at"]

        c = conn.cursor()
        c.execute("INSERT INTO tweetdata2 (tweet, date, team, GameWeek) VALUES (%s,%s,%s,%s)",
                  (tweetdb, tweetdatedb, team, gw))

        conn.commit()
        count = count+1
    print(tweet["text"])
    print(tweet["created_at"])

print(count)
print(myResponse["next"])




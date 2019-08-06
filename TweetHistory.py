from requests_oauthlib import OAuth1Session
import MySQLdb


#        replace mysql.server with "localhost" if you are running via your own server!
#                        server       MySQL username	MySQL pass  Database name.
conn = MySQLdb.connect("localhost","root","","premierpredict",use_unicode=True, charset='utf8')

# consumer key, consumer secret, access token, access secret.
ckey = ""
csecret = ""
atoken = ""
asecret = ""


twitter = OAuth1Session(ckey,
                        client_secret=csecret,
                        resource_owner_key=atoken,
                        resource_owner_secret=asecret)
# , "next": ""

gw = 39
team = 'NUFC'

url = 'https://api.twitter.com/1.1/tweets/search/30Day/PP30Days.json'
query = '{"query": "#%s", "fromDate": "201805011200", "toDate": "201805091230"}' % team
# query = '{"query": "#%s", "fromDate": "201804291200", "toDate": "201805041030", "next": "%s"}' % (team, next)
count = 49
myResponse = twitter.post(url, query).json()
print(myResponse)
tweets = myResponse["results"]
for tweet in tweets:
    if not tweet["retweeted"] and 'RT @' not in tweet["text"] and tweet["lang"] == "en":
        print(tweet["text"], tweet["created_at"])
        tweetdb=tweet["text"]
        tweetdatedb=tweet["created_at"]

        c = conn.cursor()
        c.execute("INSERT INTO tweetdata (tweet, date, team, GameWeek) VALUES (%s,%s,%s,%s)",
                  (tweetdb, tweetdatedb, team, gw))

        conn.commit()
        count = count+1
    print(tweet["text"])
    print(tweet["created_at"])

print(count)
print(myResponse["next"])
nextpg = myResponse["next"]

while count < 101:
    query = '{"query": "#%s", "fromDate": "201805011200", "toDate": "201805091230", "next": "%s"}' % (team, nextpg)
    myResponse = twitter.post(url, query).json()
    print(myResponse)
    tweets = myResponse["results"]
    for tweet in tweets:
        if not tweet["retweeted"] and 'RT @' not in tweet["text"] and tweet["lang"] == "en":
            print(tweet["text"], tweet["created_at"])
            tweetdb=tweet["text"]
            tweetdatedb=tweet["created_at"]

            c = conn.cursor()
            c.execute("INSERT INTO tweetdata (tweet, date, team, GameWeek) VALUES (%s,%s,%s,%s)",
                      (tweetdb, tweetdatedb, team, gw))

            conn.commit()
            count = count+1

        print(tweet["text"])
        print(tweet["created_at"])
    print(count)
    nextpg = myResponse["next"]
print(count)

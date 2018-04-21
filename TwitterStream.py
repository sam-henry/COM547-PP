from sklearn.externals import joblib
from tweepy import OAuthHandler
import tweepy
import MySQLdb

def dictfetchall(cursor):
    # "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


gw = 35

vectorizer = joblib.load('Classifiers/vectorizer.pkl')
log_model = joblib.load('Classifiers/log_model.pkl')
sgd_model = joblib.load('Classifiers/sgd_model.pkl')
svm_model = joblib.load('Classifiers/svm_model.pkl')
ext_model = joblib.load('Classifiers/ext_model.pkl')
mnnb_model = joblib.load('Classifiers/mnnb_model.pkl')
voting_model = joblib.load('Classifiers/voting_model.pkl')

models = [
    {'Name': 'LRScore', 'clf': log_model, 'Total': 'LRPTotal'},
    {'Name': 'SGDScore', 'clf': sgd_model, 'Total': 'SGDPTotal'},
    {'Name': 'SVMScore', 'clf': svm_model, 'Total': 'SVMPTotal'},
    {'Name': 'EXTScore', 'clf': ext_model, 'Total': 'EXTPTotal'},
    {'Name': 'MNNBScore', 'clf': mnnb_model, 'Total': 'MNNBPTotal'},
    {'Name': 'VotingScore', 'clf': voting_model, 'Total': 'VotingPTotal'}
]

conn = MySQLdb.connect("localhost", "root", "", "premierpredict", use_unicode=True, charset='utf8')
cursor = conn.cursor()

q_teams = 'SELECT * FROM pp_teams'
cursor.execute(q_teams)
teams = dictfetchall(cursor)


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if not status.retweeted and 'RT @' not in status.text and status.lang == 'en':
            entities = status.entities
            hashtags = entities['hashtags']
            tags = []
            for ht in hashtags:
                tags.append(ht['text'].upper())

            for team in teams:
                for tag in tags:
                    if tag == team['ShortTeamName']:
                        data = [status.text]
                        features = vectorizer.transform(data)
                        q_totals_check = "SELECT * FROM pp_Total WHERE TeamName = '%s' " \
                                   "AND GameWeek = %s" % (team['TeamName'], gw)
                        results = cursor.execute(q_totals_check)
                        if not results:
                            q_totals_insert= "INSERT INTO pp_Total(TeamName, GameWeek) " \
                                       "Values ('%s', %s)" % (team['TeamName'], gw)
                            cursor.execute(q_totals_insert)
                            conn.commit()
                        q_tweet_total = "Select TweetTotal FROM pp_total WHERE TeamName = '%s' " \
                                   "AND GameWeek = %s" % (team['TeamName'], gw)
                        cursor.execute(q_tweet_total)
                        counter = dictfetchall(cursor)
                        ctotal = 0
                        for count in counter:
                            ctotal = count['TweetTotal']
                            if not count['TweetTotal']:
                                ctotal = 0
                            elif count['TweetTotal']:
                                ctotal = count['TweetTotal']
                            ctotal += 1
                        for model in models:
                            pred = model['clf'].predict(features)
                            q_positive_total= "Select %s AS PTotal FROM pp_total WHERE TeamName = '%s' " \
                                       "AND GameWeek = %s" % (model['Total'], team['TeamName'], gw)
                            cursor.execute(q_positive_total)
                            counter = dictfetchall(cursor)
                            ptotal = 0
                            for count in counter:
                                ptotal = count['PTotal']
                                if not count['PTotal']:
                                    ptotal = 0
                                elif count['PTotal']:
                                    ptotal = count['PTotal']
                                ptotal += pred
                            q_total_update = "UPDATE pp_total SET TweetTotal=%s, %s = %s WHERE TeamName = '%s' " \
                                      "AND GameWeek = %s" % (ctotal, model['Total'], ptotal[0], team['TeamName'], gw)
                            cursor.execute(q_total_update)
                            conn.commit()
                            if ctotal != 0:
                                clf_score = ptotal / ctotal
                                q_sentimentscore_check = "SELECT * FROM pp_sentimentscore WHERE TeamName = '%s'" \
                                           " AND GameWeek = %s" % (team['TeamName'], gw)
                                results = cursor.execute(q_sentimentscore_check)
                                if not results:
                                    q_sentimentscore_insert = "INSERT INTO pp_sentimentscore(TeamName, GameWeek) " \
                                               "Values ('%s', %s)" % (team['TeamName'], gw)
                                    cursor.execute(q_sentimentscore_insert)
                                    conn.commit()
                                q_sentimentscore_update = "UPDATE pp_sentimentscore SET %s = %s WHERE GameWeek = %s " \
                                        "AND TeamName = '%s'" % (model['Name'], clf_score[0], gw, team['TeamName'])
                                cursor.execute(q_sentimentscore_update)
                                conn.commit()
                                print(clf_score)
            return True


    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False

        # returning non-False reconnects the stream, with backoff.


# consumer key, consumer secret, access token, access secret.
ckey = "UJ5LUyq9RZ8dAUiwRvKtHgOWi"
csecret = "oUc85NGKuIqTenTtyLkkOf40e1ohcXoUVx4gyQEG9giMhZfdoi"
atoken = "526890392-8WQJBhoB53f69mtnIjaPYCAaLBlYrtCXxUAqGTXc"
asecret = "utmPGRtezzrUvzP6qzTBLYstqy5cYP0XDMNEGH5UqEn8k"

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)

twitterListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=twitterListener)
teamHT = []
for t in teams:
    teamHT.append(t['TeamHashtag'])

myStream.filter(track=teamHT, async=True)


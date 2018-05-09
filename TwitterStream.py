from sklearn.externals import joblib
from tweepy import OAuthHandler
import tweepy
import MySQLdb

# function to convert db response from the db
def dictfetchall(cursor):
    # "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# set the game week value
gw = 38

# import the classification models and vectorizer from file
vectorizer = joblib.load('Classifiers/vectorizer.pkl')
log_model = joblib.load('Classifiers/log_model.pkl')
sgd_model = joblib.load('Classifiers/sgd_model.pkl')
svm_model = joblib.load('Classifiers/svm_model.pkl')
ext_model = joblib.load('Classifiers/ext_model.pkl')
mnnb_model = joblib.load('Classifiers/mnnb_model.pkl')
voting_model = joblib.load('Classifiers/voting_model.pkl')

# create dictionary to store classification models and fieldnames
models = [
    {'Name': 'LRScore', 'clf': log_model, 'Total': 'LRPTotal'},
    {'Name': 'SGDScore', 'clf': sgd_model, 'Total': 'SGDPTotal'},
    {'Name': 'SVMScore', 'clf': svm_model, 'Total': 'SVMPTotal'},
    {'Name': 'EXTScore', 'clf': ext_model, 'Total': 'EXTPTotal'},
    {'Name': 'MNNBScore', 'clf': mnnb_model, 'Total': 'MNNBPTotal'},
    {'Name': 'VotingScore', 'clf': voting_model, 'Total': 'VotingPTotal'}
]

# connect to the database
conn = MySQLdb.connect("localhost", "root", "", "premierpredict", use_unicode=True, charset='utf8')
cursor = conn.cursor()
# retrieve team data and store in variable teams
q_teams = 'SELECT * FROM pp_teams'
cursor.execute(q_teams)
teams = dictfetchall(cursor)

# declare class for the stream listener
class MyStreamListener(tweepy.StreamListener):
    # function to handle tweets from the streaming api
    def on_status(self, status):
        # filter tweets returned from the stream
        if not status.retweeted and 'RT @' not in status.text and status.lang == 'en':
            # retrieve the hashtags from the tweet
            entities = status.entities
            hashtags = entities['hashtags']
            tags = []
            for ht in hashtags:
                tags.append(ht['text'].upper())
            # loop through each team
            for team in teams:
                # loop through each tweet hashtag
                for tag in tags:
                    #if the hashtag belongs to the team
                    if tag == team['ShortTeamName']:
                        #retrieve the data
                        data = [status.text]
                        print(data)
                        # prepare the data for classification
                        features = vectorizer.transform(data)
                        # check if there is count total data in the db
                        q_totals_check = "SELECT * FROM pp_Total WHERE TeamName = '%s' " \
                                         "AND GameWeek = %s" % (team['TeamName'], gw)
                        results = cursor.execute(q_totals_check)
                        # if not totals created in the db create one.
                        if not results:
                            q_totals_insert = "INSERT INTO pp_Total(TeamName, GameWeek) " \
                                              "Values ('%s', %s)" % (team['TeamName'], gw)
                            cursor.execute(q_totals_insert)
                            conn.commit()
                        # retriev total tweet count from the database
                        q_tweet_total = "Select TweetTotal FROM pp_total WHERE TeamName = '%s' " \
                                        "AND GameWeek = %s" % (team['TeamName'], gw)
                        cursor.execute(q_tweet_total)
                        counter = dictfetchall(cursor)
                        # initialise ctotal to 0
                        ctotal = 0
                        # cycle through ctotal validate and set ctotal to  count value
                        for count in counter:
                            ctotal = count['TweetTotal']
                            if not count['TweetTotal']:
                                ctotal = 0
                            elif count['TweetTotal']:
                                ctotal = count['TweetTotal']
                            # increment the ctotal value by 1
                            ctotal += 1
                        # loop through the model object
                        for model in models:
                            # classify the tweet sentiment and store the output in pred
                            pred = model['clf'].predict(features)
                            # retrive the positive tweet count from the database for the model and store it in counter
                            q_positive_total = "Select %s AS PTotal FROM pp_total WHERE TeamName = '%s' " \
                                               "AND GameWeek = %s" % (model['Total'], team['TeamName'], gw)
                            cursor.execute(q_positive_total)
                            counter = dictfetchall(cursor)
                            # initialise ptotal to 0
                            ptotal = 0
                            # loop over the data, validate and store it in ptotal
                            for count in counter:
                                ptotal = count['PTotal']
                                if not count['PTotal']:
                                    ptotal = 0
                                elif count['PTotal']:
                                    ptotal = count['PTotal']
                                # add the pred value to ptotal
                                ptotal += pred
                            # input both the ctotal and ptotal back into the pp_total table
                            q_total_update = "UPDATE pp_total SET TweetTotal=%s, %s = %s WHERE TeamName = '%s' AND " \
                                             "GameWeek = %s" % (ctotal, model['Total'], ptotal[0], team['TeamName'], gw)
                            cursor.execute(q_total_update)
                            conn.commit()
                            # check the ctotal does not = 0
                            if ctotal != 0:
                                # calculate the sentiment score from te count totals
                                clf_score = ptotal / ctotal
                                # check if there is an entry in the db for sentiment score
                                q_sentimentscore_check = "SELECT * FROM pp_sentimentscore WHERE TeamName = '%s'" \
                                                         " AND GameWeek = %s" % (team['TeamName'], gw)
                                results = cursor.execute(q_sentimentscore_check)
                                # if not create an entry in the db for sentiment score
                                if not results:
                                    q_sentimentscore_insert = "INSERT INTO pp_sentimentscore(TeamName, GameWeek) " \
                                                              "Values ('%s', %s)" % (team['TeamName'], gw)
                                    cursor.execute(q_sentimentscore_insert)
                                    conn.commit()
                                # add the new sentiment score to the database
                                q_sentimentscore_update = "UPDATE pp_sentimentscore SET %s = %s " \
                                                          "WHERE GameWeek = %s AND TeamName = '%s'"\
                                                          % (model['Name'], clf_score[0], gw, team['TeamName'])
                                cursor.execute(q_sentimentscore_update)
                                conn.commit()
                                # output the score to the data base
                                # print(clf_score)
            # return true to the twitter stream to retrieve the next tweet.
            return True

# function to handle error codes returned from the Twitter stream
    def on_error(self, status_code):
        # if error code is 420
        if status_code == 420:
            # disconnect the stream
            return False
        # if not then reconnect to the stream,


# Data to produce the authentication token for connecting to the twitter api
ckey = "UJ5LUyq9RZ8dAUiwRvKtHgOWi"
csecret = "oUc85NGKuIqTenTtyLkkOf40e1ohcXoUVx4gyQEG9giMhZfdoi"
atoken = "526890392-8WQJBhoB53f69mtnIjaPYCAaLBlYrtCXxUAqGTXc"
asecret = "utmPGRtezzrUvzP6qzTBLYstqy5cYP0XDMNEGH5UqEn8k"
# create authentication token
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
# pass the token to the API to create connection
api = tweepy.API(auth)
# create object from the stream listener object
twitterListener = MyStreamListener()
# call the api and pass the object to myStream
myStream = tweepy.Stream(auth=api.auth, listener=twitterListener)
# retrive the team hastags from the team object and store them in teamHT list object
teamHT = []
for t in teams:
    teamHT.append(t['TeamHashtag'])
# pass the team hashtags to the stream connection as the filter parameter
myStream.filter(track=teamHT, async=True)

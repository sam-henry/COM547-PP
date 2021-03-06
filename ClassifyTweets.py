from sklearn.externals import joblib
import MySQLdb


# import saved modela and vectorizer from file
vectorizer = joblib.load('Classifiers/vectorizer.pkl')
log_model = joblib.load('Classifiers/log_model.pkl')
sgd_model = joblib.load('Classifiers/sgd_model.pkl')
svm_model = joblib.load('Classifiers/svm_model.pkl')
ext_model = joblib.load('Classifiers/ext_model.pkl')
mnnb_model = joblib.load('Classifiers/mnnb_model.pkl')
voting_model = joblib.load('Classifiers/voting_model.pkl')

# function to convert db responses to dictionaries
def dictfetchall(cursor):
    # "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# database connection
conn = MySQLdb.connect("localhost","root","","premierpredict",use_unicode=True, charset='utf8')

# prepare a cursor object using cursor() method
cursor = conn.cursor()
gws = [39]
# retrieve all the teams from the DB
teams = []
sqlquery = "SELECT TeamName, ShortTeamName FROM pp_teams"
cursor.execute(sqlquery)
teams = dictfetchall(cursor)
# print the team data to the console
for team in teams:
    print(team['TeamName'])
    print(team['ShortTeamName'])
    # create a dictionary object to contain models
models = [
    {'Name': 'LRScore', 'clf': log_model},
    {'Name': 'SGDScore', 'clf': sgd_model},
    {'Name': 'SVMScore', 'clf': svm_model},
    {'Name': 'EXTScore', 'clf': ext_model},
    {'Name': 'MNNBScore', 'clf': mnnb_model},
    {'Name': 'VotingScore', 'clf': voting_model}

]

# loop through game weeks
for gw in gws:
    # loop through teams
    for team in teams:
        sqlstmt = "SELECT * FROM tweetdata WHERE GameWeek = '%s' AND Team = '%s'" % (gw, team['ShortTeamName'])
        # Execute the SQL command
        cursor.execute(sqlstmt)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        if results:

            query = "INSERT INTO pp_sentimentscore (GameWeek, TeamName) VALUES(%s,'%s')" % (gw, team['TeamName'])

            cursor.execute(query)
            conn.commit()
            for model in models:
                count = 0
                p_count = 0
                # Prepare SQL query to INSERT a record into the database
                sqlstmt = "SELECT * FROM tweetdata WHERE GameWeek = '%s' AND Team = '%s'" % (gw, team['ShortTeamName'])
                # Execute the SQL command
                cursor.execute(sqlstmt)
                # Fetch all the rows in a list of lists.
                results = cursor.fetchall()
                for row in results:
                    tweet = row[1]
                    data = [tweet]
                    features = vectorizer.transform(data)
                    pred = model['clf'].predict(features)
                    p_count += pred
                    count += 1
                if count != 0:
                    clf_score = (p_count)/count
                    # print("GameWeek %s, Team %s, model is %s,, p_count is %s, score is %s" % (gw, team, model['Name'], p_count, clf_score))

                    query = "UPDATE pp_sentimentscore SET %s = %s WHERE GameWeek = %s AND TeamName = '%s'" % (model['Name'], clf_score[0], gw, team['TeamName'])
                    cursor.execute(query)
                    conn.commit()
    #except:
    #    print("Cannot fetch results")
    # disconnect from server
conn.close()

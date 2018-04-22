import MySQLdb
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import ExtraTreesClassifier

# database connection
conn = MySQLdb.connect("localhost","root","","premierpredict",use_unicode=True, charset='utf8')

# prepare a cursor object using cursor() method
cursor = conn.cursor()
# create a model dictionary
models = [
    {'Name': 'lr', 'FieldName': 'LRPrediction'},
    {'Name': 'sgd', 'FieldName': 'SGDPrediction'},
    {'Name': 'svm', 'FieldName': 'SVMPrediction'},
    {'Name': 'ext', 'FieldName': 'EXTPrediction'},
    {'Name': 'mnnb', 'FieldName': 'MNNBPrediction'},
    {'Name': 'voting', 'FieldName': 'VotingPrediction'}

]
# create prediction classifier
etc = ExtraTreesClassifier(
    n_estimators=100,
    random_state=0,
    n_jobs=-1
)

# loop through the model object
for model in models:
    # retrieve the training data from the db
    q_pred_train_view = "Select HomeTeamScore, AwayTeamScore, Result From pp_%s_trainingset WHERE Result IS NOT NULL"\
               % (model['Name'])
    cursor.execute(q_pred_train_view)
    r = cursor.fetchall()
    # split it into features and results
    x = []
    y_train = []
    for row in r:
        home_score = row[0]
        away_score = row[1]
        result = row[2]
        data = [home_score, away_score]
        x.append(data)
        y_train.append(result)
    # scale the features
    stdsc = StandardScaler()
    x_train = stdsc.fit_transform(x)
    # train the model
    clf = etc.fit(x_train, y_train)
    # retrieve the data to be classified
    q_pred_classify_view = "Select FixtureID, HomeTeamScore, AwayTeamScore, Result From pp_%s_trainingset " \
                           "WHERE Result IS NULL" % (model['Name'])
    cursor.execute(q_pred_classify_view)
    r1 = cursor.fetchall()

    # place data returned into variables
    for row in r1:
        x_test = []
        fixture = row[0]
        home_score = row[1]
        away_score = row[2]
        data = [home_score, away_score]
        x_test.append(data)
        # scale the features
        x_test = stdsc.transform(x_test)
        # produce prediction
        y_pred = clf.predict(x_test)

        # If fixture ID is in the table update if not insert
        q_pred_check = "SELECT * FROM pp_prediction WHERE FixtureID = %s" % fixture
        cursor.execute(q_pred_check)
        r2 = cursor.fetchall()
        if r2:
            q_pred_update = "UPDATE pp_prediction SET %s = %s WHERE FixtureID = %s "\
                            % (model['FieldName'], y_pred[0], fixture)
            cursor.execute(q_pred_update)
            conn.commit()
        else:
            q_pred_insert = "INSERT INTO pp_prediction(FixtureID, %s) VALUES(%s, %s)"\
                            % (model['FieldName'], fixture, y_pred[0])
            cursor.execute(q_pred_insert)
            conn.commit()
conn.close()



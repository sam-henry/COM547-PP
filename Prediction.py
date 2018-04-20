import MySQLdb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import accuracy_score, precision_score, recall_score


#        replace mysql.server with "localhost" if you are running via your own server!
#                        server       MySQL username	MySQL pass  Database name.
conn = MySQLdb.connect("localhost","root","","premierpredict",use_unicode=True, charset='utf8')

# prepare a cursor object using cursor() method
cursor = conn.cursor()

models = [
    {'Name': 'lr', 'FieldName': 'LRPrediction'},
    {'Name': 'sgd', 'FieldName': 'SGDPrediction'},
    {'Name': 'svm', 'FieldName': 'SVMPrediction'},
    {'Name': 'ext', 'FieldName': 'EXTPrediction'},
    {'Name': 'mnnb', 'FieldName': 'MNNBPrediction'},
    {'Name': 'voting', 'FieldName': 'VotingPrediction'}

]
etc = ExtraTreesClassifier(
    n_estimators=100,
    random_state=0,
    n_jobs=-1
)


for model in models:

    q_pred_train_view = "Select HomeTeamScore, AwayTeamScore, Result From pp_%s_trainingset WHERE Result IS NOT NULL"\
               % (model['Name'])
    cursor.execute(q_pred_train_view)
    r = cursor.fetchall()

    x = []
    y_train = []
    for row in r:
        home_score = row[0]
        away_score = row[1]
        result = row[2]
        data = [home_score, away_score]
        x.append(data)
        y_train.append(result)

    stdsc = StandardScaler()
    x_train = stdsc.fit_transform(x)
    clf = etc.fit(x_train, y_train)

    q_pred_classify_view = "Select FixtureID, HomeTeamScore, AwayTeamScore, Result From pp_%s_trainingset " \
                           "WHERE Result IS NULL" % (model['Name'])
    cursor.execute(q_pred_classify_view)
    r1 = cursor.fetchall()


    for row in r1:
        x_test = []
        fixture = row[0]
        home_score = row[1]
        away_score = row[2]
        data = [home_score, away_score]
        x_test.append(data)
        x_test = stdsc.transform(x_test)
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
            # INSERT INTO `pp_prediction`(`FixtureID`, `LRPrediction`) VALUES ([value-1],[value-2])
            q_pred_insert = "INSERT INTO pp_prediction(FixtureID, %s) VALUES(%s, %s)"\
                            % (model['FieldName'], fixture, y_pred[0])
            cursor.execute(q_pred_insert)
            conn.commit()



conn.close()

    # print(model['Name'], accuracy_score(y_test, y_pred))
    #
    # print(cross_val_score(clf, x_train, y_train, cv=3, scoring="accuracy", ))
    # y_train_pred = cross_val_predict(clf, x_train, y_train, cv=3)
    # print(precision_score(y_train, y_train_pred, average=None))
    # print(recall_score(y_train, y_train_pred, average=None))



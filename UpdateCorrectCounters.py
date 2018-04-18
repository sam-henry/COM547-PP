import MySQLdb

#        replace mysql.server with "localhost" if you are running via your own server!
#                        server       MySQL username	MySQL pass  Database name.
conn = MySQLdb.connect("localhost","root","","premierpredict",use_unicode=True, charset='utf8')
# prepare a cursor object using cursor() method
cursor = conn.cursor()

sqlquery = "SELECT p.FixtureID, p.LRPrediction, p.SGDPrediction, p.SVMPrediction, p.EXTPrediction, " \
           "p.MNNBPrediction, p.VotingPrediction, r.result from pp_Prediction p INNER JOIN pp_Results r " \
           "ON r.FixtureID = p.FixtureID WHERE r.Result IS NOT NULL"
cursor.execute(sqlquery)
r1 = cursor.fetchall()

for row in r1:
    fixture = row[0]
    prediction = [
        {'FieldName': 'LRCorrect', 'pred': row[1]},
        {'FieldName': 'SGDCorrect', 'pred': row[2]},
        {'FieldName': 'SVMCorrect', 'pred': row[3]},
        {'FieldName': 'EXTCorrect', 'pred': row[4]},
        {'FieldName': 'MNNBCorrect', 'pred': row[5]},
        {'FieldName': 'VotingCorrect', 'pred': row[6]}
    ]
    result = row[7]

    for p in prediction:
        sqlquery2 = "Select * FROM pp_correct WHERE FixtureID = %s" % fixture
        cursor.execute(sqlquery2)
        r2 = cursor.fetchall()
        if not r2:
            sqlquery3 = "INSERT INTO pp_correct(FixtureID) VALUES(%s)" % fixture
            cursor.execute(sqlquery3)
            conn.commit()

        if p['pred'] == result:
            sqlquery4 = "UPDATE pp_correct SET %s = 1 WHERE FixtureID = %s" % (p['FieldName'], fixture)
        else:
            sqlquery4 = "UPDATE pp_correct SET %s = 0 WHERE FixtureID = %s" % (p['FieldName'], fixture)
        cursor.execute(sqlquery4)
        conn.commit()
conn.close()

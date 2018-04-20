import MySQLdb

#        replace mysql.server with "localhost" if you are running via your own server!
#                        server       MySQL username	MySQL pass  Database name.
conn = MySQLdb.connect("localhost","root","","premierpredict",use_unicode=True, charset='utf8')
# prepare a cursor object using cursor() method
cursor = conn.cursor()

q_pred_result = "SELECT p.FixtureID, p.LRPrediction, p.SGDPrediction, p.SVMPrediction, p.EXTPrediction, " \
           "p.MNNBPrediction, p.VotingPrediction, r.result from pp_Prediction p INNER JOIN pp_Results r " \
           "ON r.FixtureID = p.FixtureID WHERE r.Result IS NOT NULL"
cursor.execute(q_pred_result)
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
        q_correct_check = "Select * FROM pp_correct WHERE FixtureID = %s" % fixture
        cursor.execute(q_correct_check)
        r2 = cursor.fetchall()
        if not r2:
            q_correct_insert = "INSERT INTO pp_correct(FixtureID) VALUES(%s)" % fixture
            cursor.execute(q_correct_insert)
            conn.commit()

        if p['pred'] == result:
            correct = 1
        else:
            correct = 0
        q_correct_update = "UPDATE pp_correct SET %s = %s WHERE FixtureID = %s" % (p['FieldName'], correct, fixture)
        cursor.execute(q_correct_update)
        conn.commit()
conn.close()

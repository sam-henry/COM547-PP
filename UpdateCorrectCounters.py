import MySQLdb
# database connector
conn = MySQLdb.connect("localhost","root","","premierpredict",use_unicode=True, charset='utf8')
# prepare a cursor object using cursor() method
cursor = conn.cursor()
# query to retrieve prediction data
q_pred_result = "SELECT p.FixtureID, p.LRPrediction, p.SGDPrediction, p.SVMPrediction, p.EXTPrediction, " \
           "p.MNNBPrediction, p.VotingPrediction, r.result from pp_Prediction p INNER JOIN pp_Results r " \
           "ON r.FixtureID = p.FixtureID WHERE r.Result IS NOT NULL"
cursor.execute(q_pred_result)
r1 = cursor.fetchall()
# pass returned prediction data into a blank dictionary object
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
    # add the result returned to result variable
    result = row[7]
    # iterate over the predicted results
    for p in prediction:
        # check if there is an entry in the table for fixture id
        q_correct_check = "Select * FROM pp_correct WHERE FixtureID = %s" % fixture
        cursor.execute(q_correct_check)
        r2 = cursor.fetchall()
        #if no entry in the db add one
        if not r2:
            q_correct_insert = "INSERT INTO pp_correct(FixtureID) VALUES(%s)" % fixture
            cursor.execute(q_correct_insert)
            conn.commit()
        # if the predicted result is the same as actual result insert 1 into the db
        if p['pred'] == result:
            correct = 1
        # if not add a 0
        else:
            correct = 0
        q_correct_update = "UPDATE pp_correct SET %s = %s WHERE FixtureID = %s" % (p['FieldName'], correct, fixture)
        cursor.execute(q_correct_update)
        conn.commit()
conn.close()

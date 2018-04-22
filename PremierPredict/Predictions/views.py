from django.shortcuts import render
import json
from django.db import connection


# function to convert DB response to dictionary
def dictfetchall(cursor):
    # "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

#query for retrieving the graph data
q_graph_data = "SELECT CAST(f.GameWeek AS CHAR) AS GameWeek, CAST(SUM(c.LRCorrect)AS UNSIGNED) AS LR," \
               " CAST(SUM(c.SGDCorrect) AS UNSIGNED) AS SGD, CAST(SUM(c.SVMCorrect) AS UNSIGNED) AS SVM," \
               " CAST(SUM(c.EXTCorrect) AS UNSIGNED) AS EXT, CAST(SUM(c.MNNBCorrect) AS UNSIGNED) AS MNNB," \
               " CAST(SUM(c.VotingCorrect) AS UNSIGNED) AS Voting FROM pp_correct c JOIN pp_fixtures f" \
               " ON f.FixtureID = c.FixtureID GROUP BY f.GameWeek"

# function to handel the voting request
def voting(request):
    # created a cursor object
    c = connection.cursor()
    # query to return prediction table data
    q_voting_table_data = "SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.VotingPrediction As Prediction " \
                          "FROM pp_fixtures f JOIN pp_prediction p ON p.FixtureID = f.FixtureID JOIN pp_results r " \
                          "ON r.FixtureID = f.FixtureID WHERE p.LRPrediction Is NOT NULL AND r.Result IS NULL"
    # execute table query
    c.execute(q_voting_table_data)
    # convert the response to a dictionary and store in fixtures
    fixtures = dictfetchall(c)
    # execute graph query
    c.execute(q_graph_data)
    # convert the response to a dictionary and store in correct
    correct = dictfetchall(c)
    # convert correct dictionary to JSON format
    correct = json.dumps(correct)
    # pass data to the index.html file
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Voting Predictions'
    }
    return render(request, 'index.html', context)


# function to handel the lr request
def lr(request):
    c = connection.cursor()
    # query to return prediction table data
    q_lr_table_data = "SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.LRPrediction As Prediction " \
                      "FROM pp_fixtures f JOIN pp_prediction p ON p.FixtureID = f.FixtureID " \
                      "JOIN pp_results r ON r.FixtureID = f.FixtureID " \
                      "WHERE p.LRPrediction Is NOT NULL AND r.Result IS NULL"
    # execute table query
    c.execute(q_lr_table_data)
    # convert the response to a dictionary and store in fixtures
    fixtures = dictfetchall(c)
    # execute graph query
    c.execute(q_graph_data)
    # convert the response to a dictionary and store in correct
    correct = dictfetchall(c)
    # convert correct dictionary to JSON format
    correct = json.dumps(correct)
    # pass data to the index.html file
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Logarithmic Regression Predictions'
    }
    return render(request, 'index.html', context)


# function to handel the SGD request
def sgd(request):
    c = connection.cursor()
    # query to return prediction table data
    q_sgd_table_data = "SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.SGDPrediction As Prediction " \
                       "FROM pp_fixtures f JOIN pp_prediction p ON p.FixtureID = f.FixtureID " \
                       "JOIN pp_results r ON r.FixtureID = f.FixtureID " \
                       "WHERE p.LRPrediction Is NOT NULL AND r.Result IS NULL"
    # execute table query
    c.execute(q_sgd_table_data)
    # convert the response to a dictionary and store in fixtures
    fixtures = dictfetchall(c)
    # execute graph query
    c.execute(q_graph_data)
    # convert the response to a dictionary and store in correct
    correct = dictfetchall(c)
    # convert correct dictionary to JSON format
    correct = json.dumps(correct)
    # pass data to the index.html file
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Stochastic Gradient Descent Predictions'
    }
    return render(request, 'index.html', context)


# function to handel the SVM request
def svm(request):
    c = connection.cursor()
    # query to return prediction table data
    q_svm_table_data = "SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.SVMPrediction As Prediction " \
                       "FROM pp_fixtures f JOIN pp_prediction p ON p.FixtureID = f.FixtureID " \
                       "JOIN pp_results r ON r.FixtureID = f.FixtureID " \
                       "WHERE p.LRPrediction Is NOT NULL AND r.Result IS NULL"
    # execute table query
    c.execute(q_svm_table_data)
    # convert the response to a dictionary and store in fixtures
    fixtures = dictfetchall(c)
    # execute graph query
    c.execute(q_graph_data)
    # convert the response to a dictionary and store in correct
    correct = dictfetchall(c)
    # convert correct dictionary to JSON format
    correct = json.dumps(correct)
    # pass data to the index.html file
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Support Vector Machine Predictions'
    }
    return render(request, 'index.html', context)


# function to handel the EXT request
def ext(request):
    c = connection.cursor()
    # query to return prediction table data
    q_ext_table_data = "SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.EXTPrediction As Prediction " \
                       "FROM pp_fixtures f JOIN pp_prediction p ON p.FixtureID = f.FixtureID JOIN pp_results r " \
                       "ON r.FixtureID = f.FixtureID WHERE p.LRPrediction Is NOT NULL AND r.Result IS NULL"
    # execute table query
    c.execute(q_ext_table_data)
    # convert the response to a dictionary and store in fixtures
    fixtures = dictfetchall(c)
    # execute graph query
    c.execute(q_graph_data)
    # convert the response to a dictionary and store in correct
    correct = dictfetchall(c)
    # convert correct dictionary to JSON format
    correct = json.dumps(correct)
    # pass data to the index.html file
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Extra Random Trees Predictions'
    }
    return render(request, 'index.html', context)

# function to handel the MNNB request
def mnnb(request):
    c = connection.cursor()
    # query to return prediction table data
    q_mnnb_table_data = "SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.MNNBPrediction As Prediction " \
                        "FROM pp_fixtures f JOIN pp_prediction p ON p.FixtureID = f.FixtureID JOIN pp_results r " \
                        "ON r.FixtureID = f.FixtureID WHERE p.LRPrediction Is NOT NULL AND r.Result IS NULL"
    # execute table query
    c.execute(q_mnnb_table_data)
    # convert the response to a dictionary and store in fixtures
    fixtures = dictfetchall(c)
    # execute graph query
    c.execute(q_graph_data)
    # convert the response to a dictionary and store in correct
    correct = dictfetchall(c)
    # convert correct dictionary to JSON format
    correct = json.dumps(correct)
    # pass data to the index.html file
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Multinomial Naive Bayes Predictions'
    }
    return render(request, 'index.html', context)

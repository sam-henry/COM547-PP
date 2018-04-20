from django.shortcuts import render
import json

from django.db import connection
from django.shortcuts import render_to_response


# Create your views here.
def dictfetchall(cursor):
    # "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


q_graph_data = "SELECT CAST(f.GameWeek AS CHAR) AS GameWeek, CAST(SUM(c.LRCorrect)AS UNSIGNED) AS LR," \
               " CAST(SUM(c.SGDCorrect) AS UNSIGNED) AS SGD, CAST(SUM(c.SVMCorrect) AS UNSIGNED) AS SVM," \
               " CAST(SUM(c.EXTCorrect) AS UNSIGNED) AS EXT, CAST(SUM(c.MNNBCorrect) AS UNSIGNED) AS MNNB," \
               " CAST(SUM(c.VotingCorrect) AS UNSIGNED) AS Voting FROM pp_correct c JOIN pp_fixtures f" \
               " ON f.FixtureID = c.FixtureID GROUP BY f.GameWeek"


def voting(request):
    c = connection.cursor()
    q_voting_table_data = "SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.VotingPrediction As Prediction " \
                          "FROM pp_fixtures f JOIN pp_prediction p ON p.FixtureID = f.FixtureID JOIN pp_results r " \
                          "ON r.FixtureID = f.FixtureID WHERE p.LRPrediction Is NOT NULL AND r.Result IS NULL"
    c.execute(q_voting_table_data)
    fixtures = dictfetchall(c)
    c.execute(q_graph_data)
    correct = dictfetchall(c)
    correct = json.dumps(correct)
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Voting Predictions'
    }
    return render(request, 'index.html', context)


def lr(request):
    c = connection.cursor()
    q_lr_table_data = "SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.LRPrediction As Prediction " \
                      "FROM pp_fixtures f JOIN pp_prediction p ON p.FixtureID = f.FixtureID " \
                      "JOIN pp_results r ON r.FixtureID = f.FixtureID " \
                      "WHERE p.LRPrediction Is NOT NULL AND r.Result IS NULL"
    c.execute(q_lr_table_data)
    fixtures = dictfetchall(c)
    c.execute(q_graph_data)
    correct = dictfetchall(c)
    correct = json.dumps(correct)
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Logarithmic Regression Predictions'
    }
    return render(request, 'index.html', context)


def sgd(request):
    c = connection.cursor()
    q_sgd_table_data = "SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.SGDPrediction As Prediction " \
                       "FROM pp_fixtures f JOIN pp_prediction p ON p.FixtureID = f.FixtureID " \
                       "JOIN pp_results r ON r.FixtureID = f.FixtureID " \
                       "WHERE p.LRPrediction Is NOT NULL AND r.Result IS NULL"
    c.execute(q_sgd_table_data)
    fixtures = dictfetchall(c)
    c.execute(q_graph_data)
    correct = dictfetchall(c)
    correct = json.dumps(correct)
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Stochastic Gradient Descent Predictions'
    }
    return render(request, 'index.html', context)


def svm(request):
    c = connection.cursor()
    q_svm_table_data = "SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.SVMPrediction As Prediction " \
                       "FROM pp_fixtures f JOIN pp_prediction p ON p.FixtureID = f.FixtureID " \
                       "JOIN pp_results r ON r.FixtureID = f.FixtureID " \
                       "WHERE p.LRPrediction Is NOT NULL AND r.Result IS NULL"
    c.execute(q_svm_table_data)
    fixtures = dictfetchall(c)
    c.execute(q_graph_data)
    correct = dictfetchall(c)
    correct = json.dumps(correct)
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Support Vector Machine Predictions'
    }
    return render(request, 'index.html', context)


def ext(request):
    c = connection.cursor()
    q_ext_table_data = "SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.EXTPrediction As Prediction " \
                       "FROM pp_fixtures f JOIN pp_prediction p ON p.FixtureID = f.FixtureID JOIN pp_results r " \
                       "ON r.FixtureID = f.FixtureID WHERE p.LRPrediction Is NOT NULL AND r.Result IS NULL"
    c.execute(q_ext_table_data)
    fixtures = dictfetchall(c)
    c.execute(q_graph_data)
    correct = dictfetchall(c)
    correct = json.dumps(correct)
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Extra Random Trees Predictions'
    }
    return render(request, 'index.html', context)


def mnnb(request):
    c = connection.cursor()
    q_mnnb_table_data = "SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.MNNBPrediction As Prediction " \
                        "FROM pp_fixtures f JOIN pp_prediction p ON p.FixtureID = f.FixtureID JOIN pp_results r " \
                        "ON r.FixtureID = f.FixtureID WHERE p.LRPrediction Is NOT NULL AND r.Result IS NULL"
    c.execute(q_mnnb_table_data)
    fixtures = dictfetchall(c)
    c.execute(q_graph_data)
    correct = dictfetchall(c)
    correct = json.dumps(correct)
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Multinomial Naive Bayes Predictions'
    }
    return render(request, 'index.html', context)

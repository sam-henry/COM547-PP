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


def voting(request):
    c = connection.cursor()
    c.execute('SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.VotingPrediction As Prediction FROM pp_fixtures f '
              'JOIN pp_prediction p ON p.FixtureID = f.FixtureID WHERE GameWeek = 31')
    fixtures = dictfetchall(c)

    c.execute('SELECT CAST(f.GameWeek AS CHAR) AS GameWeek, CAST(SUM(c.LRCorrect)AS UNSIGNED) AS LR, '
              'CAST(SUM(c.SGDCorrect) AS UNSIGNED) AS SGD, CAST(SUM(c.SVMCorrect) AS UNSIGNED) AS SVM, '
              'CAST(SUM(c.EXTCorrect) AS UNSIGNED) AS EXT, CAST(SUM(c.MNNBCorrect) AS UNSIGNED) AS MNNB, '
              'CAST(SUM(c.VotingCorrect) AS UNSIGNED) AS Voting FROM pp_correct c JOIN pp_fixtures f '
              'ON f.FixtureID = c.FixtureID GROUP BY f.GameWeek')

    correct = dictfetchall(c)
    correct = json.dumps(correct)
    # fixtures = PpFixtures.objects.filter(gameweek=31)
    # fixtures = PpFixtures.objects.raw('SELECT * FROM pp_fixtures WHERE GameWeek = 31')
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Voting Predictions'

    }

    return render(request, 'index.html', context)


def lr(request):
    c = connection.cursor()
    c.execute('SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.LRPrediction As Prediction FROM pp_fixtures f '
              'JOIN pp_prediction p ON p.FixtureID = f.FixtureID WHERE GameWeek = 31')
    fixtures = dictfetchall(c)

    c.execute('SELECT CAST(f.GameWeek AS CHAR) AS GameWeek, CAST(SUM(c.LRCorrect)AS UNSIGNED) AS LR, '
              'CAST(SUM(c.SGDCorrect) AS UNSIGNED) AS SGD, CAST(SUM(c.SVMCorrect) AS UNSIGNED) AS SVM, '
              'CAST(SUM(c.EXTCorrect) AS UNSIGNED) AS EXT, CAST(SUM(c.MNNBCorrect) AS UNSIGNED) AS MNNB, '
              'CAST(SUM(c.VotingCorrect) AS UNSIGNED) AS Voting FROM pp_correct c JOIN pp_fixtures f '
              'ON f.FixtureID = c.FixtureID GROUP BY f.GameWeek')

    correct = dictfetchall(c)
    correct = json.dumps(correct)
    # fixtures = PpFixtures.objects.filter(gameweek=31)
    # fixtures = PpFixtures.objects.raw('SELECT * FROM pp_fixtures WHERE GameWeek = 31')
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Logarithmic Regression Predictions'
    }

    return render(request, 'index.html', context)


def sgd(request):
    c = connection.cursor()
    c.execute('SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.SGDPrediction As Prediction FROM pp_fixtures f '
              'JOIN pp_prediction p ON p.FixtureID = f.FixtureID WHERE GameWeek = 31')
    fixtures = dictfetchall(c)

    c.execute('SELECT CAST(f.GameWeek AS CHAR) AS GameWeek, CAST(SUM(c.LRCorrect)AS UNSIGNED) AS LR, '
              'CAST(SUM(c.SGDCorrect) AS UNSIGNED) AS SGD, CAST(SUM(c.SVMCorrect) AS UNSIGNED) AS SVM, '
              'CAST(SUM(c.EXTCorrect) AS UNSIGNED) AS EXT, CAST(SUM(c.MNNBCorrect) AS UNSIGNED) AS MNNB, '
              'CAST(SUM(c.VotingCorrect) AS UNSIGNED) AS Voting FROM pp_correct c JOIN pp_fixtures f '
              'ON f.FixtureID = c.FixtureID GROUP BY f.GameWeek')

    correct = dictfetchall(c)
    correct = json.dumps(correct)
    # fixtures = PpFixtures.objects.filter(gameweek=31)
    # fixtures = PpFixtures.objects.raw('SELECT * FROM pp_fixtures WHERE GameWeek = 31')
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Stochastic Gradient Descent Predictions'

    }

    return render(request, 'index.html', context)


def svm(request):
    c = connection.cursor()
    c.execute('SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.SVMPrediction As Prediction FROM pp_fixtures f '
              'JOIN pp_prediction p ON p.FixtureID = f.FixtureID WHERE GameWeek = 31')
    fixtures = dictfetchall(c)

    c.execute('SELECT CAST(f.GameWeek AS CHAR) AS GameWeek, CAST(SUM(c.LRCorrect)AS UNSIGNED) AS LR, '
              'CAST(SUM(c.SGDCorrect) AS UNSIGNED) AS SGD, CAST(SUM(c.SVMCorrect) AS UNSIGNED) AS SVM, '
              'CAST(SUM(c.EXTCorrect) AS UNSIGNED) AS EXT, CAST(SUM(c.MNNBCorrect) AS UNSIGNED) AS MNNB, '
              'CAST(SUM(c.VotingCorrect) AS UNSIGNED) AS Voting FROM pp_correct c JOIN pp_fixtures f '
              'ON f.FixtureID = c.FixtureID GROUP BY f.GameWeek')

    correct = dictfetchall(c)
    correct = json.dumps(correct)
    # fixtures = PpFixtures.objects.filter(gameweek=31)
    # fixtures = PpFixtures.objects.raw('SELECT * FROM pp_fixtures WHERE GameWeek = 31')
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Support Vector Machine Predictions'

    }

    return render(request, 'index.html', context)


def ext(request):
    c = connection.cursor()
    c.execute('SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.EXTPrediction As Prediction FROM pp_fixtures f '
              'JOIN pp_prediction p ON p.FixtureID = f.FixtureID WHERE GameWeek = 31')
    fixtures = dictfetchall(c)

    c.execute('SELECT CAST(f.GameWeek AS CHAR) AS GameWeek, CAST(SUM(c.LRCorrect)AS UNSIGNED) AS LR, '
              'CAST(SUM(c.SGDCorrect) AS UNSIGNED) AS SGD, CAST(SUM(c.SVMCorrect) AS UNSIGNED) AS SVM, '
              'CAST(SUM(c.EXTCorrect) AS UNSIGNED) AS EXT, CAST(SUM(c.MNNBCorrect) AS UNSIGNED) AS MNNB, '
              'CAST(SUM(c.VotingCorrect) AS UNSIGNED) AS Voting FROM pp_correct c JOIN pp_fixtures f '
              'ON f.FixtureID = c.FixtureID GROUP BY f.GameWeek')

    correct = dictfetchall(c)
    correct = json.dumps(correct)
    # fixtures = PpFixtures.objects.filter(gameweek=31)
    # fixtures = PpFixtures.objects.raw('SELECT * FROM pp_fixtures WHERE GameWeek = 31')
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Extra Random Trees Predictions'

    }

    return render(request, 'index.html', context)


def mnnb(request):
    c = connection.cursor()
    c.execute('SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.LRPrediction As Prediction FROM pp_fixtures f '
              'JOIN pp_prediction p ON p.FixtureID = f.FixtureID WHERE GameWeek = 31')
    fixtures = dictfetchall(c)

    c.execute('SELECT CAST(f.GameWeek AS CHAR) AS GameWeek, CAST(SUM(c.LRCorrect)AS UNSIGNED) AS LR, '
              'CAST(SUM(c.SGDCorrect) AS UNSIGNED) AS SGD, CAST(SUM(c.SVMCorrect) AS UNSIGNED) AS SVM, '
              'CAST(SUM(c.EXTCorrect) AS UNSIGNED) AS EXT, CAST(SUM(c.MNNBCorrect) AS UNSIGNED) AS MNNB, '
              'CAST(SUM(c.VotingCorrect) AS UNSIGNED) AS Voting FROM pp_correct c JOIN pp_fixtures f '
              'ON f.FixtureID = c.FixtureID GROUP BY f.GameWeek')

    correct = dictfetchall(c)
    correct = json.dumps(correct)
    # fixtures = PpFixtures.objects.filter(gameweek=31)
    # fixtures = PpFixtures.objects.raw('SELECT * FROM pp_fixtures WHERE GameWeek = 31')
    context = {
        'fixtures': fixtures,
        'correct': correct,
        'name': 'Multinomial Naive Bayes Predictions'

    }

    return render(request, 'index.html', context)

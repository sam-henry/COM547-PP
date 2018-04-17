from django.shortcuts import render
from Predictions.models import PpPrediction, PpFixtures, PpCorrect
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

def home(request):
    c = connection.cursor()
    c.execute('SELECT f.FixtureID, f.HomeTeam, f.AwayTeam, p.VotingPrediction As Prediction FROM pp_fixtures f '
              'JOIN pp_prediction p ON p.FixtureID = f.FixtureID WHERE GameWeek = 31')
    fixtures = dictfetchall(c)
    # fixtures = PpFixtures.objects.filter(gameweek=31)
    # fixtures = PpFixtures.objects.raw('SELECT * FROM pp_fixtures WHERE GameWeek = 31')
    context = {
        'fixtures': fixtures,

    }

    return render(request, 'index.html', context)

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class PpFixtures(models.Model):
    fixtureid = models.AutoField(db_column='FixtureID', primary_key=True)  # Field name made lowercase.
    gameweek = models.IntegerField(db_column='GameWeek')  # Field name made lowercase.
    datetime = models.TextField(db_column='DateTime')  # Field name made lowercase.
    hometeam = models.TextField('PpTeams', db_column='HomeTeam')  # Field name made lowercase.
    awayteam = models.TextField('PpTeams', db_column='AwayTeam')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pp_fixtures'


class PpTeams(models.Model):
    teamname = models.CharField(db_column='TeamName', primary_key=True, max_length=40)  # Field name made lowercase.
    shortteamname = models.CharField(db_column='ShortTeamName', max_length=10)  # Field name made lowercase.
    teamhashtag = models.CharField(db_column='TeamHashtag', max_length=11)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pp_teams'


class PpPrediction(models.Model):
    fixtureid = models.IntegerField(PpFixtures, db_column='FixtureID', primary_key=True)  # Field name made lowercase.
    lrprediction = models.IntegerField(db_column='LRPrediction', blank=True, null=True)  # Field name made lowercase.
    sgdprediction = models.IntegerField(db_column='SGDPrediction', blank=True, null=True)  # Field name made lowercase.
    svmprediction = models.IntegerField(db_column='SVMPrediction', blank=True, null=True)  # Field name made lowercase.
    extprediction = models.IntegerField(db_column='EXTPrediction', blank=True, null=True)  # Field name made lowercase.
    mnnbprediction = models.IntegerField(db_column='MNNBPrediction', blank=True, null=True)  # Field name made lowercase.
    votingprediction = models.IntegerField(db_column='VotingPrediction', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pp_prediction'


class PpResults(models.Model):
    fixtureid = models.IntegerField(PpFixtures, db_column='FixtureID', primary_key=True)  # Field name made lowercase.
    result = models.IntegerField(db_column='Result', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pp_results'


class PpCorrect(models.Model):
    fixtureid = models.IntegerField('PpFixtures', db_column='FixtureID', primary_key=True)  # Field name made lowercase.
    lrcorrect = models.IntegerField(db_column='LRCorrect', blank=True, null=True)  # Field name made lowercase.
    sgdcorrect = models.IntegerField(db_column='SGDCorrect', blank=True, null=True)  # Field name made lowercase.
    svmcorrect = models.IntegerField(db_column='SVMCorrect', blank=True, null=True)  # Field name made lowercase.
    extcorrect = models.IntegerField(db_column='EXTCorrect', blank=True, null=True)  # Field name made lowercase.
    mnnbcorrect = models.IntegerField(db_column='MNNBCorrect', blank=True, null=True)  # Field name made lowercase.
    votingcorrect = models.IntegerField(db_column='VotingCorrect', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pp_correct'

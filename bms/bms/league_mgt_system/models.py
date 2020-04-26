from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db.models import Sum, Count


class User(AbstractUser, models.Model):
    is_admin = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)
    is_player = models.BooleanField(default=False)

    no_of_logins = models.BigIntegerField(default=0)
    is_online = models.BooleanField(default=False)
    total_time_spent = models.BigIntegerField(default=0)

class Team(models.Model):
    name = models.TextField(max_length=100, null=False, blank=False, unique=True)
    coach = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def get_avg_team_score(self):
        total_score = PlayerPerformance.objects.filter(team_id=self.id).aggregate(Sum('score'))['score__sum']
        no_of_games = PlayerPerformance.objects.values('game_id').filter(team_id=self.id).distinct().count()
        return total_score / no_of_games

class Player(models.Model):
    height = models.CharField(max_length=5)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_no_of_matches(self):
        return PlayerPerformance.objects.values('game_id').filter(player_id=self.id).distinct().count()

    def get_player_avg_score(self):
        total_score = PlayerPerformance.objects.filter(player_id=self.id).aggregate(Sum('score'))['score__sum']
        if total_score is None:
            return 0
        no_of_matches = PlayerPerformance.objects.values('game_id').filter(player_id=self.id).distinct().count()
        return total_score / no_of_matches

class Tournament(models.Model):
    name = models.TextField(max_length=100, null= False, blank=False)

class Round(models.Model):
    round = models.IntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING, related_name="rounds")

class Game(models.Model):
    game_date = models.DateField()
    round = models.ForeignKey(Round, on_delete=models.DO_NOTHING)
    winning_team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="winning_team")
    losing_team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="losing_team")
    winning_team_score = models.IntegerField(default=0)
    losing_team_score = models.IntegerField(default=0)
    player_performance = models.ManyToManyField(Player, through='PlayerPerformance')

class PlayerPerformance(models.Model):
    score = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)

from django.core.management import BaseCommand
from bms.league_mgt_system.models import User, Tournament, Round, Team, Player, Game, PlayerPerformance
import random
from random import randint
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Generate User Data"

    def handle(self, *args, **kwargs):
        team_names = ['Atlanta Hawks', 'Boston CelticsBoston Celtics', 'Brooklyn Nets',
                      'Charlotte HornetsCharlotte Hornets',
                      'Chicago BullsChicago Bulls', 'Cleveland CavaliersCleveland Cavaliers',
                      'Dallas MavericksDallas Mavericks',
                      'Denver NuggetsDenver Nuggets', 'Detroit PistonsDetroit Pistons',
                      'Golden State WarriorsGolden State Warriors',
                      'Houston RocketsHouston Rockets', 'Indiana PacersIndiana Pacers', 'LA ClippersLA Clippers',
                      'Los Angeles LakersLos Angeles Lakers', 'Memphis GrizzliesMemphis Grizzlies',
                      'Miami HeatMiami Heat']

        first_names = ['Melvin', 'Hunt', 'Chris', 'Jent', 'Greg']
        last_names = ['Foster', 'Marlon', 'Garnett', 'Matt', 'Hill']

        # Create league admin
        User.objects.create_user(username='admin', password='admin',
                                 first_name='admin', last_name='admin', is_admin=True,
                                 no_of_logins=4, total_time_spent=random.randint(4, 20), is_online=True)

        tournament = Tournament.objects.create(name="USA NBA League")

        Round.objects.create(round=1, tournament=tournament)
        Round.objects.create(round=2, tournament=tournament)
        Round.objects.create(round=3, tournament=tournament)
        Round.objects.create(round=4, tournament=tournament)

        for i in range(0, 16):
            team_name = team_names[i]
            coach_user = User.objects.create_user(username='coach-{}'.format(i), password='coach-pass',
                                                  first_name=random.choice(first_names),
                                                  last_name=random.choice(last_names),
                                                  is_coach=True, no_of_logins=random.randint(0, 10),
                                                  total_time_spent=random.randint(4, 10),
                                                  is_online=bool(random.randint(0, 1)))

            team = Team.objects.create(name=team_name, coach=coach_user)

            for p in range(0, 10):
                player_user = User.objects.create_user(username='user-{}-{}'.format(i, p), password='user-pass',
                                                       first_name=random.choice(first_names),
                                                       last_name=random.choice(last_names), is_player=True,
                                                       no_of_logins=random.randint(0, 3),
                                                       total_time_spent=random.randint(4, 8),
                                                       is_online=bool(random.randint(0, 1)))

                Player.objects.create(height='{} feet {} inches'.format(randint(5, 6), randint(0, 11)), team=team,
                                      user=player_user)

        # generate random games and scores
        teams = list(Team.objects.all());
        round = 1
        tournament_start_date = datetime.strptime("2020-01-01", "%Y-%m-%d")
        next_round_teams = []

        while teams:
            try:
                tournament_round = Round.objects.get(round=round)
            except Round.DoesNotExist:
                tournament_round = Round.objects.create(round=round, tournament=tournament)

            team1 = teams.pop()
            team2 = teams.pop()

            game = Game.objects.create(
                game_date=tournament_start_date, winning_team=team1, losing_team=team2, round=tournament_round)

            # get 5 players form team 1
            team1_players = team1.player_set.all()
            random.shuffle(list(team1_players))
            team2_players = team2.player_set.all()
            random.shuffle(list(team2_players))

            team1_score = 0
            team2_score = 0

            for t in range(0, 5):
                score = random.randint(2, 4)
                team1_score += score
                PlayerPerformance.objects.create(game=game,
                                                 player=team1_players[t], score=score, team=team1)

            for t in range(0, 5):
                score = random.randint(0, 2)
                team2_score += score
                PlayerPerformance.objects.create(game=game,
                                                 player=team2_players[t], score=score, team=team2)

            game = Game.objects.get(pk=game.pk)
            game.winning_team_score = team1_score
            game.losing_team_score = team2_score
            game.save()

            next_round_teams.append(team1)

            tournament_start_date = tournament_start_date + timedelta(days=1)

            if len(teams) == 1:
                next_round_teams.insert(0, teams.pop())

            if len(teams) == 0 and len(next_round_teams) == 1:
                break

            # next round
            if len(teams) == 0:
                # level up
                round += 1
                teams = next_round_teams
                next_round_teams = []

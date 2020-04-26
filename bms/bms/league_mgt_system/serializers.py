from rest_framework import serializers
from bms.league_mgt_system.models import Tournament, Round, User, Game, Team, Player, PlayerPerformance
from rest_framework.fields import ReadOnlyField


class TeamUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name']

class TeamSerializer(serializers.ModelSerializer):
	coach = TeamUserSerializer()
	team_avg_score = ReadOnlyField(source='get_avg_team_score')
	class Meta:
		model = Team
		fields = ['id', 'name', 'coach', 'team_avg_score']

class PlayerSerializer(serializers.ModelSerializer):
	user = TeamUserSerializer()
	no_of_matches = ReadOnlyField(source='get_no_of_matches', default=0)
	player_avg_score = ReadOnlyField(source='get_player_avg_score', default=0)

	class Meta:
		model = Player
		fields = ['id', 'height', 'user', 'no_of_matches', 'player_avg_score']

class PlayerPerformanceSerializer(serializers.ModelSerializer):
	player = PlayerSerializer()
	class Meta:
		model = PlayerPerformance
		fields = ['score', 'player']

class GameSerializer(serializers.ModelSerializer):
	winning_team = TeamSerializer()
	losing_team =  TeamSerializer()
	class Meta:
		model = Game
		fields = ['game_date', 'winning_team', 'losing_team', 'winning_team_score', 'losing_team_score']

class RoundSerializer(serializers.ModelSerializer):
	games = GameSerializer(source="game_set", many=True)
	class Meta:
		model = Round
		fields = ['round', 'games']

class TournamentSerializer(serializers.ModelSerializer):
	rounds = RoundSerializer(many=True)
	class Meta:
		model = Tournament
		fields = ['name', 'rounds']

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name',
				  'no_of_logins', 'is_online', 'total_time_spent', 'is_player', 'is_coach', 'is_admin']


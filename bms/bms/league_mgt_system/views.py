from rest_framework.views import APIView
from rest_framework.response import Response
from bms.league_mgt_system.models import Tournament, User, Team, Player
from bms.league_mgt_system.serializers import TournamentSerializer, UserSerializer, TeamSerializer, PlayerSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import Http404


class TournamentViews(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        tournaments = Tournament.objects.all()
        serializer = TournamentSerializer(tournaments, many=True)
        return Response(serializer.data)

class LoginViews(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        logins = User.objects.all();
        serializer = UserSerializer(logins, many=True)
        return Response(serializer.data)

class TeamViews(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        teams = Team.objects.all();
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

class TeamDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        players = Player.objects.filter(team_id=pk)
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

class PlayerDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Player.objects.get(pk=pk)
        except Player.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        player = self.get_object(pk)
        serializer = PlayerSerializer(player)
        return Response(serializer.data)

class UserDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

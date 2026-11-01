from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import leaderboard_views, squad_views, views

urlpatterns = [
    path("teams/", views.TeamList.as_view()),
    path("players/", views.PlayerList.as_view()),
    path("players/<int:pk>/", views.PlayerDetail.as_view()),
    path("register/", squad_views.RegisterView.as_view()),
    path("login/", obtain_auth_token),
    path("squad/", squad_views.SquadView.as_view()),
    path("leaderboard/", leaderboard_views.LeaderboardView.as_view()),
]
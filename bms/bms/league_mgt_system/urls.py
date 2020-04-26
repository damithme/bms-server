"""firstproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from bms.league_mgt_system import views

urlpatterns = [
    path('tournaments/', views.TournamentViews.as_view()),
    path('logins/', views.LoginViews.as_view()),
    path('teams/', views.TeamViews.as_view()),
    path('teams/<int:pk>/', views.TeamDetail.as_view()),
    path('players/<int:pk>/', views.PlayerDetail.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

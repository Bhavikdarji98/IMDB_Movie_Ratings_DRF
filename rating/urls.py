from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from rating import views, api

urlpatterns = [
    path('signup/', views.UserCreate.as_view()),
    path('movies/', api.MovieDetails.as_view()),
]


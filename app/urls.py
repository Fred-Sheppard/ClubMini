from django.views.static import serve
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test/", views.test, name='test'),
    path("login/", views.login, name='login'),
    path("discover/", views.discover, name='discover'),
    path("login/sign_up/", views.sign_up, name='sign_up'),
    path("profile/",views.profile, name='profile'),
]

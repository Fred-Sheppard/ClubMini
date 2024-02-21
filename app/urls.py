from django.views.static import serve
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test/", views.test, name='test'),
    path("login/", views.login, name='login'),
    path("discover/", views.discover, name='discover'),
    path("create_event/", views.create_event, name='create_event'),
    path("promt_club/", views.promt_club, name='promt_club'),
    path("create_club/", views.create_club, name='create_club'),
    path("student_dashboard/", views.student_dashboard, name='student_dashboard')
]

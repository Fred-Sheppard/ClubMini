from django.views.static import serve
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test/", views.test, name='test'),
    path("login/", views.login, name='login'),
    path("discover/", views.discover, name='discover'),
    path("student_dashboard/", views.student_dashboard, name='student_dashboard')
]

from django.urls import path
from . import views


urlpatterns = [
    path('vulnerabilities/',views.get_all, name='vulnerability-list'),
]
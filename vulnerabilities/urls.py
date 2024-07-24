from django.urls import path
from . import views


urlpatterns = [
    path('vulnerabilities/',views.get_all, name='vulnerability-list'),
    path('vulnerabilities/summary/',views.vulnerability_severity_summary, name='vulnerability-list'),
    path('vulnerabilities/excluding-fixed/' ,views.get_queryset, name='vulnerability'),
]
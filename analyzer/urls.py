from django.urls import path
from . import views

urlpatterns = [
    path('analyze-url/', views.analyze_url, name='analyze_url'),
]

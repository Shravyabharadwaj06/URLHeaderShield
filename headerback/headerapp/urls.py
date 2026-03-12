from django.contrib import admin
from django.urls import path
from headerapp import views

urlpatterns=[
    path("",views.index,name='headerapp'),
    path("analyze/", views.analyze_url, name='analyze_url'),
    path("report/", views.report_url, name='report_url'),
    path("search/", views.search_reports, name='search_reports'),
    path("vote/", views.vote_report, name='vote_report'),
    path("remove_vote/", views.remove_vote, name='remove_vote'),
]
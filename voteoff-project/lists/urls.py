from django.urls import path
from . import views

app_name = 'lists'
urlpatterns = [
    path('lists/<str:key>/', views.index, name='index'),
    path('lists/create', views.createcontest, name='createcontest'),
    path('lists/mycontests/<str:key>/', views.mycontests, name='mycontests'),
    path('lists/details/<int:contest_id>/', views.detail, name='detail'),
    path('lists/results/<int:contest_id>/', views.results, name='results'),
    path('lists/vote/<int:contest_id>/', views.vote, name='vote'),
    path('lists/addusers/<int:contest_id>/', views.addusers, name='addusers'),
    path('lists/deletecontest/<int:contest_id>/', views.deleteContest, name='deleteContest'),
]
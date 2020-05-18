from django.urls import path
from . import views

app_name = 'lists'
urlpatterns = [
    path('lists/', views.index, name='index'),
    path('lists/create', views.createlist, name='createlist'),
    path('lists/mylists', views.mylists, name='mylists'),
    path('lists/details/<int:contest_id>/', views.detail, name='detail'),
    path('lists/results/<int:contest_id>/', views.results, name='results'),
    path('lists/vote/<int:contest_id>/', views.vote, name='vote'),
    path('lists/addusers/<int:contest_id>/', views.addusers, name='addusers'),
]
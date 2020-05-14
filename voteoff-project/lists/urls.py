from django.urls import path
from . import views

app_name = 'lists'
urlpatterns = [
    path('lists/', views.index, name='index'),
    path('lists/create', views.createlist, name='createlist'),
    path('lists/mylists', views.mylists, name='mylists'),
    path('lists/details/<int:question_id>/', views.detail, name='detail'),
    path('lists/results/<int:question_id>/', views.results, name='results'),
    path('lists/<int:question_id>/vote/', views.vote, name='vote')
]

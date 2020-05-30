from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.registeracc, name="registeracc"),
    path('login/', views.loginuser, name="loginuser"),
    path('logout/', views.logoutuser, name="logoutuser"),
    path('profile/', views.userprofile, name="userprofile"),
    path('profile/edit/', views.editprofile, name="editprofile"),
]
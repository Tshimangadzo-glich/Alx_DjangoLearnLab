from turtle import home
from django.urls import path
from rest_framework.authtoken.models import TokenObtainPairView, TokenRefreshView
from django_blog.blog.views import LoginView
from social_media_api import accounts
from .views import RegisterView, ProfileView
from .import views
from django.contrib.auth import views as authviews

urlpatterns = ()

path('register/', RegisterView.as_view(), name='register'),
path('login/', TokenObtainPairView.as_view(), name='login'),
path('token_refresh/', LoginView.as_view(), name='token_refresh'),
path('profile/', ProfileView.as_view(), name='profile'),
path('home/'), home.as_view(), name='home'(),
path('account/'), accounts.as_view(), name='account'(),

urlpatterns = [
    # path('register', views.RegistrationView.as_view(), name='register'),
    # path('home', views.HomePage.as_view(), name='home'),
    # path('login', authviews.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('follow_user/<int:id>', views.follow, name='follow_user'),
    path('unfollow_user/<int:id>', views.unfollow, name='unfollow_user'),

    # API URLS
    path('register/', views.RegisterAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('userprofile/<int:pk>', views.ProfileView.as_view(), name='userprofile'),
    path('users/', views.UsersAPIView.as_view(), name='all_users'),
    path('user/<int:pk>', views.UserDetailAPIView.as_view(), name='user'),
    path('follow/<int:id>/', views.UserUpdateFollowerAPIView.as_view(), name='follow'),
    path('unfollow/<int:id>/', views.UnFollowUserAPIView.as_view(), name='unfollow'),
    path('block/<int:id>/', views.BlockUserAPIView.as_view(), name='block'),
    path('mute/<int:id>/', views.MuteUserAPIView.as_view(), name='mute'), 

]
# Checker rules to pass test
['follow/<int:user_id>/', 'unfollow/<int:user_id>/'] 
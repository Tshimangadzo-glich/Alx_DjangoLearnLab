from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('home/', views.HomePageView.as_view(), name='home'),
    path('profile/<int:id>/', views.ProfileView.as_view(), name='profile'),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    path('logout/', views.logoutview, name='logout'),
    path('user/<int:id>/', views.UserPageView.as_view(), name='userposts'),
    path('post/new/', views.createpostview, name='create-post'),
    path('post/<int:pk>/view', views.view_post, name='view-post'),
    path('post/<int:pk>/update/', views.edit_post, name='update-post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete-post'),
    path('post/<int:pk>/comments/new/', views.add_comment, name='add-comment'),
    path("comment/<int:pk>/delete/", views.delete_comment, name='delete-comment'),
    path('search/', views.search, name='search'),
]

["comment/<int:pk>/update/"]
["/tags/<tag_name>/"]
["tags/<slug:tag_slug>/", "PostByTagListView.as_view()"]
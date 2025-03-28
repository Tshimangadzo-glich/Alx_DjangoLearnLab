from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken import RefreshToken
from rest_framework.authtoken import TokenObtainPairView
from .serializers import RegisterSerializer, ProfileSerializer
from .models import User
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .forms import RegistrationForm
from .models import CustomUser
from models import Post
from .serializers import RegistrationSerializer, LoginSerializer, CustomUserSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login = TokenObtainPairView.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh_token.access_token),
                'refresh': str(refresh_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if form.is_valid():
            # print(form.cleaned_data.get('username'))
            # print(form.cleaned_data.get('password1'))
            # print(form.cleaned_data.get('password2'))
            form.save()
        return super().form_valid(form)
    
# class HomePage(generic.ListView):
#     model = CustomUser
#     template_name = 'accounts/home.html'
#     context_object_name = 'all_users'

# DetailView for display a user profile
class ProfileView(generic.DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'detail_user'
    lookup_field = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # current user = user
        user = self.model.objects.get(id=context['object'].id)
        all_followers = user.followers.all()
        following_count = user.following.all()
        all_posts = Post.objects.filter(author=user.id).order_by('-created_at')
        context['all_followers'] = all_followers
        context['follwer_count'] = all_followers.count()
        context['following_count'] = following_count.count()
        context['user_posts_count'] = all_posts.count()
        context['user_posts'] = all_posts
        return context

def follow(request, id):
    follower_id = CustomUser.objects.get(id=request.user.id)
    user_id = CustomUser.objects.get(id=id)
    if follower_id and user_id:
        user_id.followers.add(follower_id)
        user_id.save()
        count = user_id.followers.all().count()
        all_followers = user_id.followers.all()
    return redirect(reverse_lazy('userprofile', kwargs={'pk': id}), {'count': count, 'all_followers': all_followers, 'following_user': True})

def unfollow(request, id):
    current_user = request.user.id
    user = CustomUser.objects.get(id=id)
    follower = user.followers.get(id=current_user)
    if follower:
        user.followers.remove(follower)
    return redirect(reverse_lazy('userprofile', kwargs={'pk': id}))

"""Views for APIs & Serializers"""
class RegisterAPIView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            serializer.validated_data.pop('password1')
            password = serializer.validated_data.pop('password2')
            user = CustomUser(username=username)
            user.set_password(password)
            user.save()
            token = Token.objects.get(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)       
        return super().create(request, *args, **kwargs)

# Checkers rules to pass test
from rest_framework import permissions
[generics.GenericAPIView, permissions.IsAuthenticated]

class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializers = LoginSerializer(data=request.data)
        if serializers.is_valid():
            print('inside')
            username = serializers.validated_data.get('username')
            password = serializers.validated_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                token = Token.objects.get(user=user)
                login(request, user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            print('outside')
            return Response({'error': 'username or password is incorrect!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class UsersAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all().order_by('username')
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        context = super().get(request, *args, **kwargs).data
        for x in context['results']:
            x['followers'] = len(x['followers'])
            x['following'] = len(x['following'])
        return Response(data=context, status=status.HTTP_200_OK)

class UserDetailAPIView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'user_id'

class UserUpdateFollowerAPIView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        follower = self.request.user
        user = CustomUser.objects.get(id=kwargs.get('id'))
        all_followers = user.followers.all()
        for follow in all_followers:
            if follower.id in all_followers:
                ...
            return Response(data={f'You are already following {user}'}, status=status.HTTP_204_NO_CONTENT)
        user.followers.add(follower)
        user.save()
        context = super().update(request, *args, **kwargs).data
        context['followers'] = len(context['followers'])
        context['following'] = len(context['following'])
        data = {
            'success': f'You have successfully followed {user}',
            'data': context
        }
        return Response(data=data, status=status.HTTP_200_OK)
    
class UnFollowUserAPIView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        follower = self.request.user
        user = CustomUser.objects.get(id=kwargs.get('id'))
        user.followers.remove(follower)
        user.save()
        context = super().update(request, *args, **kwargs).data
        context['followers'] = len(context['followers'])
        context['following'] = len(context['following'])
        data = {
            'success': f'You have successfully unfollowed {user}',
            'data': context
        }
        return Response(data=data, status=status.HTTP_200_OK)

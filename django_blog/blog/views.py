from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, UserProfileForm, CreatePostForm, UpdatePostForm, CommentForm, SearchForm
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import generic
from .models import Post, Comment, Tag
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.
class HomePageView(LoginRequiredMixin, generic.ListView, FormView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'all_posts'
    form_class = SearchForm
    # Redirect unauthenticated users to login page
    login_url = 'login'
    redirect_field_name = 'next'
    ordering = ['-published_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.kwargs)
        context['count'] = Comment.objects.all().count()
        return context
    
    def get_queryset(self):
        context = super().get_queryset().prefetch_related('tags')  
        return context      

class RegisterView(FormView):
    template_name = 'blog/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            login(request=self.request, user=user)
        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'blog/login.html'
    form_class = LoginForm
    success_url = 'home'

    def form_valid(self, form):
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            print(user)
            if user is None:
                raise form.ValidationError('Incorrect email or password!')
            login(self.request, user=user)
            print('logged user in')
            return super().form_valid(form)

 
class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'blog/profile.html'
    pk_url_kwarg = 'id'
    # Redirect Unauthenticated user
    login_url = reverse_lazy('login')
    context_object_name = 'user'

    def get_queryset(self):
        user_id = self.request.user.id
        user = super().get_queryset().filter(id=user_id)
        print(user)
        return user
    
@login_required
def updateprofile(request):
    id = request.user.id
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            user = User.objects.get(id=id)
            if user:
                user.username = username
                user.email = email
                user.save()
                print("User updated to:", username, email)
                return redirect('profile')
    form = UserProfileForm()
    return render(request, 'blog/updateprofile.html', {'form': form})

def logoutview(request):
    logout(request)
    return redirect('login')

class UserPageView(LoginRequiredMixin, generic.ListView):
    template_name = 'blog/user_posts.html'
    model = Post
    context_object_name = 'user_posts'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        author_id = self.kwargs['id']
        user_posts = super().get_queryset().filter(author=author_id)
        return user_posts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()  # Add the form to the context
        # To pass the author's name for each post creator
        author = self.kwargs.get('id')
        context['author'] = User.objects.get(id=author).username
        return context
    

[generic.CreateView, 'blog/post_create.html']
[generic.UpdateView, 'blog/post_list.html']
[generic.DeleteView, 'blog/post_detail.html']
[UserPassesTestMixin, 'blog/post_delete.html', 'blog/post_edit.html']
["CommentCreateView", "CommentUpdateView", "CommentDeleteView"]
@login_required(login_url=reverse_lazy('login'))
def createpostview(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form.save_m2m()
            print('Post saved!')
            return redirect('home')
    form = CreatePostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def edit_post(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(id=pk)
        if post:
            form = UpdatePostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('home')
        form = UpdatePostForm(instance=post)
        return render(request, 'blog/edit_post.html', {'form': form, 'post': post})
    
@login_required
def delete_post(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(id = pk)
        if post and post.author == request.user:
            post.delete()
    return redirect ('home')

@login_required
def view_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        if post:
            form = CommentForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data['content'])
                return redirect('home')
    all_comments = Comment.objects.filter(post=post)
    form = CommentForm()
    return render(request, 'blog/view_post.html', {'form': form, 'post': post, 'all_comments': all_comments, 'post_author': post.author.username})

@login_required
def add_comment(request, pk):
    print(pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            post = Post.objects.get(id=pk)
            user_id = User.objects.get(id=request.user.id)
            comment = form.save(commit=False) # Do not save yet
            comment.post = post
            comment.author = user_id
            comment.content = content
            comment.save() # Now you can save
            return redirect('view-post', pk)
    form = CommentForm()
    return redirect('view-post', pk, {'form': form})

@login_required
def delete_comment(request, pk):
    if request.method == 'POST':
        comment = Comment.objects.get(id=pk)
        post_id = comment.post.id
        print(post_id)
        print(comment.content)
        if comment and (request.user.id == comment.author.id):
            comment.delete()
            return redirect('view-post', post_id)
    return HttpResponse("All good")

@login_required
def search(request):
    query = request.GET.get('q', '')  # Get search term from URL query parameter
    posts = Post.objects.all()  # Default: show all posts
    
    if query:
        print(query)
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)  # Fix: Searching for tag names
        ).distinct()  # Avoid duplicate posts if multiple fields match

    return render(request, 'blog/search_results.html', {'all_posts': posts, 'query': query})
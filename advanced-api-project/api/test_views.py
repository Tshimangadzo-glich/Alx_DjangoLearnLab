from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase
from rest_framework import status
from .models import Author, Book
from .views import ListView, CreateView, UpdateView, DeleteView

# Create your tests here.

class BookAPITest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client.login(username="limah_t", email="limah@gmail.com")
        self.user = User.objects.create_superuser(username="limah", password="password123")
        self.author = Author.objects.create(id=1, name="temitope")
        self.author_id = Author.objects.get(id=1)

    """Test for ListView"""
    def test_get_all_books(self):
        request = self.factory.get('/api/books/')
        response = ListView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """Test for CreateView"""
    def test_post_book(self):
        data = {'title': 'Python', 'publication_year': 2022, 'author': self.author.id}
        request = self.factory.post(path='/api/books/create/', data=data)
        force_authenticate(request, user=self.user)
        response = CreateView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    """Test for UpdateView for put"""
    def test_put_book(self):
        self.book = Book.objects.create(id=1, title='Python', publication_year=2022, author=self.author_id)
        data = {'id': self.book.id, 'title': 'Python2', 'publication_year': 2023, 'author': 1}
        request = self.factory.put(path='/api/books/update/', data=data)
        force_authenticate(request, user=self.user)
        response = UpdateView.as_view()(request, pk=self.book.id)
        print(response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    """Test for UpdateView for patch"""
    def test_patch_book(self):
        self.book = Book.objects.create(id=1, title='Python', publication_year=2022, author=self.author_id)
        data = {'id': self.book.id, 'title': 'Python', 'publication_year': 2023, 'author': 1}
        request = self.factory.patch(path='/api/books/update/', data=data)
        force_authenticate(request, user=self.user)
        response = UpdateView.as_view()(request, pk=self.book.id)
        print(response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    """Test for DestroyView for patch"""
    def test_delete_book(self):
        self.book = Book.objects.create(id=1, title='Python', publication_year=2022,author=self.author_id)
        data = {'id': self.book.id, 'title': 'Python', 'publication_year': 2023, 'author': 1}
        request = self.factory.delete(path='/api/books/delete/', data=data)
        force_authenticate(request, user=self.user)
        response = DeleteView.as_view()(request, pk=self.book.id)
        print(response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    """Test for filtering by title"""  
    def test_for_filtering_by_title(self):
        request = self.factory.get('/api/books/', {'title':'Python'})
        response = ListView.as_view() (request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    """Test for filtering by author"""
    def test_for_filtering_by_author(self):
        request = self.factory.get('/api/books/', {'author_id':1})
        response = ListView.as_view() (request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """Test for filtering by publication_year"""
    def test_for_filtering_by_publication_year(self):
        request = self.factory.get('/api/books/', {'publication_year':2023})
        response = ListView.as_view() (request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
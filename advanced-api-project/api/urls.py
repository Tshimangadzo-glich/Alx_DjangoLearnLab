from django.urls import path
from . import views

urlpatterns = [
    # List all the books [GET]
    path("books/", views.ListView.as_view()),
    # Retrieve book by pk [GET]
    path("books/<int:pk>/", views.DetailView.as_view()),
    # Create book [POST]
    path("books/create/", views.CreateView.as_view()),
    # Update a book by pk [PUT/PATCH]
    path("books/update/<int:pk>/", views.UpdateView.as_view()),
    # Delete a book by pk [DELETE]
    path("books/delete/<int:pk>/", views.DeleteView.as_view())
]
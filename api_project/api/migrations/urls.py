from django.urls import path, include
from .views import BookList, BookViewSet, CustomAuthToken
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  
    # Include the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)),  # This includes all routes registered with the router
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('custom-token/', CustomAuthToken.as_view(), name='custom_auth_token')
]
The ListView accepts user request, enables both authenticated and unauthenticated users get data of all books from database which is the GET method, using the BookSerializer class defined to serialize the django models objects to json file for user as response.

The DetailView accepts user request, enables both authenticated and unauthenticated users retrieve each book data with the respective id from the database which is the GET method, using the BookSerializer class defined to serialize the django models objects to json file for user as response.

The CreateView accepts user request, enables only authenticated users to create a book which is the POST method, using the BookSerializer class defined to serialize the django models objects to json file then validate the update, and save to database.

The UpdateView accepts user request, enables only authenticated users to update a book data with the respective id, which is the PUT/PATCH method, using the BookSerializer class defined to serialize the django models objects to json file then validate the update, and save to database.

The DeleteView accepts user request, enables only authenticated users to delete a book data with the respective id, which is the DELETE method, using the BookSerializer class defined to serialize the django models objects to json file then delete the data.

# Implementation of Filtering, Searching, and Ordering in views

The ListView has some features that enables user to filter, search, and order by book fields
1. The filter_backends is set to a list of classes containing [DjangoFilterBackends, filters.SearchFilter, filters.OrderingFilter]
the filterset_fields is set to the list of fields to be filtered ['title', 'author', 'publication_year'], if argument is not found, it will return empty queryset([])
the filterset_fields is case-sensitive
example param in postman: 
# http://127.0.0.1:8000/api/books?title=Python, http://127.0.0.1:8000/api/books?author=1, http://127.0.0.1:8000/api/books?publication_year=2023

2. The search_fields is set to the list of fields to be searched by ['title', 'author__id']
the relationship lookup action is implemented using "author__id" to allow using search with the author id as it's a one-to-many relationship field, the search_fields is case-insensitive
example param in postman
# http://127.0.0.1:8000/api/books?search=django, http://127.0.0.1:8000/api/books?search=1

3. The ordering_fields is set to "__all__", this will allow user to search results by any field of the Book model, and particularly the title, and publication_year field.
example param in postman
# http://127.0.0.1:8000/api/books?ordering=title, http://127.0.0.1:8000/api/books?ordering=-title, http://127.0.0.1:8000/api/books?ordering=author, http://127.0.0.1:8000/api/books?ordering=-author, http://127.0.0.1:8000/api/books?ordering=publication_year, http://127.0.0.1:8000/api/books?ordering=-publication_year
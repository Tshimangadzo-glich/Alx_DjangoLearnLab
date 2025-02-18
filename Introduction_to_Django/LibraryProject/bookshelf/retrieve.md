from bookshelf.models import Book
Book = Book.objects.get(title='1984')
print(Book.title)

print("Title:", Book.title)
print("Author:", Book.author)
print("publication_year:", Book.publication_year)

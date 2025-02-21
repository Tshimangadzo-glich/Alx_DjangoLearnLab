from relationship_app.models import Author, Book, BookReview, Publisher

def query_books_by_author(author_name):
    author = Author.objects.get(first_name=author_name.split()[0], last_name=author_name.split()[1])
    books = Book.objects.filter(author=author)
    return books

def list_all_books():
    books = Book.objects.all()
    return books

def retrieve_librarian(library_name):
    book_review = BookReview.objects.get(book__title=library_name)
    return book_review


from models import model
  class Author(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Book(models.model):
        title = models.CharField(max_length=200)
        author = models.ForeignKey(Author, on_delete = models.CASCADE)
        publication_year = models.IntergerField()

    def __str__(self):
        return self.title

    class Publisher(models.model):
        name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class BookPublisher(models.model):
        book = models.Foreignkey(Book, on_delete = models.CASCADE)
        Publisher = models.ForeignKey(Publisher, on_delete = models.CASCADE)

    def __str__(self:)
        return f"{self.book.title} - {self.Publisher.name}"

    class Bookview(models.model):
        book = models.OneToOneField(Book, on_delete = models.CASCADE)
        review = models.TextField()

    def __str__(self):
        return f"Review for {self.book.title}"
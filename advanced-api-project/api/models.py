from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="book")

    def clean(self):
        """Ensure publication_year is not in the future"""
        from datetime import datetime
        current_year = datetime.now().year
        if self.publication_year > current_year:
            raise ValidationError({'publication_year': 'Publication year cannot be in the future.'})

    def __str__(self):
        return self.title
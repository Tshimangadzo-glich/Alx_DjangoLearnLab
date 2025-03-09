from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=15, null=False, blank=False)
    author = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return f"(self.id)"
    
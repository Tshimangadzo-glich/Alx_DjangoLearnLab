from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Book
        fields = ["id", "title", "author"]

        def validate_data(self, obj):
            value = obj.title.capitalize()
            return super().save(value)
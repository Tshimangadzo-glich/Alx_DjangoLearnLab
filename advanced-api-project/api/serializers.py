from .models import Book, Author
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    """Serialize Book with the fields to be displayed"""
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """Ensure publication_year is not in the future"""
        from datetime import datetime
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError('Publication year cannot be in the future.')
        return value
    
class AuthorSerializer(serializers.ModelSerializer):
    """Book Serializer nested to bind all the books each author has created"""
    book = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['name']
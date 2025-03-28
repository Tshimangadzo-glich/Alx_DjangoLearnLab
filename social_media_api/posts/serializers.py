from .models import Post, Comment
from accounts.models import CustomUser
from rest_framework import serializers
from django.core.exceptions import ValidationError

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    """The validate attrs will get the initial data before validation"""
    def validate(self, attrs):
        current_user_id = self.context['request'].user.id
        author_id = attrs['author'].id
        if author_id != current_user_id:
            raise ValidationError(message={'author': 'You\'re not permitted to update this post, only the owner can!'})
        return super().validate(attrs)

    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, attrs):
        print("I'm in serializer class")
        current_user_id = self.context['request'].user.id
        author_id = attrs['author'].id
        print(current_user_id, author_id)
        print(CustomUser.objects.values())
        if author_id != current_user_id:
            print(True)
            raise ValidationError(message={'author': 'You\'re not permitted to modify this comment, only the owner can!'})
        return super().validate(attrs)
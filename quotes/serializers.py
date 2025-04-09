from rest_framework import serializers
from .models import User, Book, Quote

class UserSerializer(serializers.Serializer):
    uid = serializers.CharField(read_only=True)  # Read-only since it's auto-generated
    username = serializers.CharField(max_length=255)

    def create(self, validated_data):
        user = User(username=validated_data['username']).save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance

class BookSerializer(serializers.Serializer):
    uid = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)

    def create(self, validated_data):
        book = Book(title=validated_data['title'], author=validated_data['author']).save()
        return book

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance

class QuoteSerializer(serializers.Serializer):
    uid = serializers.CharField(read_only=True)
    text = serializers.CharField(max_length=1000)
    preview = serializers.CharField(read_only=True)
    timestamp = serializers.CharField(read_only=True)
    posted_by = serializers.SerializerMethodField()  # Use SerializerMethodField
    references = serializers.SerializerMethodField()  # Use SerializerMethodField

    def get_posted_by(self, obj):
        user = obj.posted_by.single()  # Fetch the connected User
        if user:
            return UserSerializer(user).data
        return None

    def get_references(self, obj):
        book = obj.references.single()  # Fetch the connected Book
        if book:
            return BookSerializer(book).data
        return None

    def create(self, validated_data):
        # Not used here; handled in view
        pass

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()  # preview auto-updates via save()
        return instance
    
    
class QuoteCreateSerializer(serializers.Serializer):
    user_uid = serializers.CharField()
    book_uid = serializers.CharField()
    text = serializers.CharField(max_length=1000)
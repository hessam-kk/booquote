from rest_framework import serializers
from .models import User, Book, Quote, ReadRel
from datetime import datetime

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
    
    
# Serializer for the READ relationship
class ReadSerializer(serializers.Serializer):
    date_of_finishing = serializers.DateField()
    score = serializers.IntegerField(min_value=1, max_value=5)
    duration_of_reading = serializers.FloatField(min_value=0.0)  # In days
    notes = serializers.CharField(max_length=500, required=False, allow_blank=True)

    def create(self, validated_data):
        user_uid = self.context['user_uid']
        book_uid = self.context['book_uid']
        user = User.nodes.get(uid=user_uid)
        book = Book.nodes.get(uid=book_uid)

        # Create or update the READ relationship
        read_rel = user.read.connect(book, {
            'date_of_finishing': validated_data['date_of_finishing'],
            'score': validated_data['score'],
            'duration_of_reading': validated_data['duration_of_reading'],
            'notes': validated_data.get('notes', '')
        })
        return read_rel
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Book, Quote
from .serializers import UserSerializer, BookSerializer, QuoteSerializer, QuoteCreateSerializer
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def create_user(request):
    permission_classes = [IsAuthenticated]  # Ensure authentication

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        book = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def post_quote(request):
    serializer = QuoteCreateSerializer(data=request.data)
    if serializer.is_valid():
        user_uid = serializer.validated_data['user_uid']
        book_uid = serializer.validated_data['book_uid']

        user = User.nodes.get_or_none(uid=user_uid)
        book = Book.nodes.get_or_none(uid=book_uid)

        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if book is None:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        quote = Quote(text=serializer.validated_data['text']).save()
        quote.posted_by.connect(user)
        quote.references.connect(book)
        return Response(QuoteSerializer(quote).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_quotes(request):
    quotes = Quote.nodes.all()
    serializer = QuoteSerializer(quotes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_quote(request, id):
    quote = Quote.nodes.get_or_none(id=uid)
    if quote:
        return Response(QuoteSerializer(quote).data)
    return Response({"error": "Quote not found"}, status=status.HTTP_404_NOT_FOUND)
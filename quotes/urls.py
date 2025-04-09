from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.create_user, name='create_user'),
    path('books/', views.create_book, name='create_book'),
    path('quotes/', views.post_quote, name='post_quote'),
    path('quotes/', views.get_all_quotes, name='get_all_quotes'),
    path('quotes/<str:id>/', views.get_quote, name='get_quote'),
]
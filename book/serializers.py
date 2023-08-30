from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "inventory", "cover", "daily_fee")


class BookListSerializer(BookSerializer):
    class Meta(BookSerializer.Meta):
        fields = ("id", "title", "author", "daily_fee")

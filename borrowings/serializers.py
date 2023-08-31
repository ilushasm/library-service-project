from rest_framework import serializers

from book.serializers import BookSerializer, BookListSerializer
from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user",
        )
        read_only_fields = (
            "id",
            "actual_return_date",
        )


class BorrowingListSerializer(BorrowingSerializer):
    book = BookListSerializer(many=False, read_only=True)

    class Meta(BorrowingSerializer.Meta):
        fields = ("id", "book", "actual_return_date", "user")
        read_only_fields = ("__all__",)

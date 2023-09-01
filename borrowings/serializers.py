from datetime import datetime

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from book.serializers import BookSerializer
from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(BorrowingSerializer, self).validate(attrs=attrs)
        book = attrs["book"]
        Borrowing.validate_borrowing(
            book=book, exception_to_raise=ValidationError
        )
        return data

    def create(self, validated_data) -> Borrowing:
        book = validated_data["book"]

        with transaction.atomic():
            self.is_valid(raise_exception=True)

            book.inventory -= 1
            book.save()

            borrowing = Borrowing.objects.create(
                user=validated_data["user"],
                book=book,
                expected_return_date=validated_data["expected_return_date"],
            )
            return borrowing

    class Meta:
        model = Borrowing
        fields = ("id", "book", "expected_return_date")


class BorrowingListSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "user",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )


class BorrowingReturnSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data) -> Borrowing:
        book = instance.book
        validated_data["actual_return_date"] = (
            datetime.today().date().strftime("%Y-%m-%d")
        )

        with transaction.atomic():
            self.is_valid(raise_exception=True)
            instance.actual_return_date = validated_data["actual_return_date"]
            book.inventory += 1
            instance.save()
            book.save()
            return instance

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "user",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )
        read_only_fields = (
            "id",
            "user",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )

from django.db import transaction
from rest_framework import viewsets, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from book.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingListSerializer


class BorrowingViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingSerializer
        return BorrowingListSerializer

    def create(self, request, *args, **kwargs) -> Response:
        user = request.user
        book_id = int(request.data.get("book"))
        expected_return_date = request.data.get("expected_return_date")

        if not book_id or book_id < 1:
            raise ValidationError({"message": "Choose a valid book"})

        book = Book.objects.get(id=book_id)
        Borrowing.validate_borrowing(
            book=book, exception_to_raise=ValidationError
        )
        data = {
            "user": user.id,
            "book": book_id,
            "expected_return_date": expected_return_date,
        }

        with transaction.atomic():
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            book.inventory -= 1
            book.save()
            serializer.validated_data["user"] = user
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

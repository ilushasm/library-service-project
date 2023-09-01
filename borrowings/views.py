from typing import Type

from django.db.models import QuerySet
from rest_framework import viewsets, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from book.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingReturnSerializer,
)


class BorrowingViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "create":
            return BorrowingSerializer
        if self.action == "borrowing_return":
            return BorrowingReturnSerializer
        return BorrowingListSerializer

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        current_user = self.request.user

        if self.action == "list":
            is_active = self.request.query_params.get("is_active")

            if is_active is not None:
                if is_active == "True":
                    queryset = queryset.exclude(
                        actual_return_date__isnull=False
                    )
                elif is_active == "False":
                    queryset = queryset.exclude(
                        actual_return_date__isnull=True
                    )

            if current_user.is_staff:
                user_id = self.request.query_params.get("user_id")
            else:
                user_id = current_user.id

            if user_id:
                queryset = queryset.filter(user_id=user_id)

        return queryset

    def perform_create(self, serializer) -> None:
        user = self.request.user
        book_id = int(self.request.data.get("book"))

        if not book_id or book_id < 1:
            raise ValidationError({"message": "Choose a valid book"})
        book = Book.objects.get(id=book_id)
        serializer.save(user=user, book=book)

    @action(
        methods=["POST"],
        detail=True,
        url_path="borrowing-return",
        permission_classes=(IsAuthenticated,),
    )
    def borrowing_return(self, request, pk: int = None) -> Response:
        borrowing = self.get_object()

        if borrowing.actual_return_date is not None:
            raise ValidationError(
                {"message": "This borrowing already returned"}
            )

        if borrowing.user != self.request.user:
            raise ValidationError(
                {"message": "You can not return someone else's borrowings"}
            )

        serializer = self.get_serializer(
            instance=borrowing, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from typing import Type

from rest_framework import viewsets, serializers
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
)
from rest_framework_simplejwt.authentication import JWTAuthentication

from book.models import Book
from book.serializers import BookSerializer, BookListSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]
        elif self.action == "retrieve":
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

    def get_serializer_class(self) -> Type[serializers.Serializer]:
        if self.action == "list":
            return BookListSerializer
        return BookSerializer

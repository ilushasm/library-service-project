from typing import Type

from django.db.models import QuerySet
from rest_framework import viewsets, mixins
from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingListSerializer


class BorrowingListRetrieveView(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        filter_params = self.request.query_params

        if filter_params:
            user_id = filter_params.get("user_id")
            is_active = (
                True if filter_params.get("is_active") == "True" else False
            )

            if user_id:
                queryset = queryset.filter(user_id=user_id)

            if is_active is not None:
                queryset = queryset.filter(
                    actual_return_date__isnull=is_active
                )

        return queryset

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return BorrowingListSerializer
        return BorrowingSerializer

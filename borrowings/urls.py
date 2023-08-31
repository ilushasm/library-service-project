from django.urls import path
from rest_framework.routers import DefaultRouter

from borrowings.views import BorrowingViewSet

router = DefaultRouter()
router.register("", BorrowingViewSet)

urlpatterns = [
    # path("", BorrowingListCreateView.as_view(), name="borrowing-list-create"),
] + router.urls

app_name = "borrowings"

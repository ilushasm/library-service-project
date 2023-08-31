from django.urls import path
from rest_framework.routers import DefaultRouter

from borrowings.views import BorrowingListRetrieveView

router = DefaultRouter()
router.register("", BorrowingListRetrieveView)

urlpatterns = router.urls

app_name = "borrowings"

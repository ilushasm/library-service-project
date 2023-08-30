from django.urls import path

from rest_framework import routers

from book.views import BookViewSet

router = routers.DefaultRouter()
router.register(prefix="books", viewset=BookViewSet)

urlpatterns = [] + router.urls

app_name = "book"

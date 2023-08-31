from django.db import models
from django.contrib.auth import get_user_model

from book.models import Book


class Borrowing(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="borrowings", on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        Book, related_name="borrowings", on_delete=models.CASCADE
    )
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(null=True)
    actual_return_date = models.DateField(null=True)

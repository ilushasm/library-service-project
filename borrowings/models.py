from django.db import models
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

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

    @staticmethod
    def validate_borrowing(book: Book, exception_to_raise) -> None:
        if book.inventory < 1:
            raise exception_to_raise(
                {"message": "Inventory for this book is depleted"}
            )

    def clean(self) -> None:
        Borrowing.validate_borrowing(
            book=self.book,
            exception_to_raise=ValidationError,
        )

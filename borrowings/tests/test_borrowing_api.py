from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from book.models import Book
from borrowings.models import Borrowing


def sample_book(**params) -> Book:
    defaults = {
        "title": "Test",
        "author": "Test",
        "inventory": 1,
        "cover": "HARD",
        "daily_fee": 10.00,
    }
    defaults.update(**params)
    return Book.objects.create(**defaults)


def sample_borrowing(**params) -> Borrowing:
    defaults = {
        "user": None,
        "book": sample_book(),
    }
    defaults.update(**params)
    return Borrowing.objects.create(**defaults)


def sample_user(super_user: bool = True, **params) -> get_user_model():
    defaults = {"email": "admin@myproject.com", "password": "password"}
    defaults.update(**params)
    if super_user:
        return get_user_model().objects.create_superuser(**defaults)
    return get_user_model().objects.create_user(**defaults)


class BorrowingReturnTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)
        self.book = sample_book()
        self.borrowing = sample_borrowing(user=self.user, book=self.book)

    def test_borrowing_return_valid(self) -> None:
        self.assertIsNone(self.borrowing.actual_return_date)

        response = self.client.post(
            f"/borrowings/{self.borrowing.id}/borrowing-return/",
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.borrowing.refresh_from_db()
        self.assertIsNotNone(self.borrowing.actual_return_date)
        self.assertEqual(self.borrowing.book.inventory, 2)

    def test_borrowing_return_already_returned(self) -> None:
        self.borrowing.actual_return_date = datetime.today()
        self.borrowing.save()

        response = self.client.post(
            f"/borrowings/{self.borrowing.id}/borrowing-return/",
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"], "This borrowing already returned"
        )

    def test_borrowing_return_wrong_user(self) -> None:
        another_user = sample_user(
            super_user=False,
            email="another@user.com",
            password="anotherpassword",
        )
        self.client.force_authenticate(user=another_user)

        response = self.client.post(
            f"/borrowings/{self.borrowing.id}/borrowing-return/",
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"],
            "You can not return someone else's borrowings",
        )


class BorrowingCreateTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = sample_user(
            super_user=False, email="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.book = sample_book()
        self.tomorrow = datetime.today().date() + timedelta(days=1)

    def test_borrowing_create_valid(self) -> None:
        initial_inventory = self.book.inventory

        data = {
            "book": self.book.id,
            "expected_return_date": self.tomorrow.strftime("%Y-%m-%d"),
        }

        response = self.client.post(
            "/borrowings/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 1)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, initial_inventory - 1)

    def test_borrowing_create_invalid_book(self) -> None:
        data = {
            "book": 9999,
            "expected_return_date": self.tomorrow.strftime("%Y-%m-%d"),
        }

        response = self.client.post(
            "/borrowings/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("book", response.data)

    def test_borrowing_create_missing_expected_return_date(self) -> None:
        data = {
            "book": self.book.id,
        }

        response = self.client.post(
            "/borrowings/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("expected_return_date", response.data)

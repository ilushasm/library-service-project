from django.db import models


class Book(models.Model):
    class BookCover(models.TextChoices):
        SOFT = "SOFT"
        HARD = "HARD"

    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    inventory = models.PositiveIntegerField()
    cover = models.CharField(
        max_length=4, choices=BookCover.choices, default=BookCover.HARD
    )
    daily_fee = models.DecimalField(decimal_places=2, max_digits=7)

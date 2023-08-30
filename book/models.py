from django.db import models


class Book(models.Model):
    class BookCover(models.TextChoices):
        SOFT = "SOFT"
        HARD = "HARD"

    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    inventory = models.PositiveIntegerField()
    cover = models.CharField(max_length=4, choices=BookCover.choices)
    daily_fee = models.DecimalField()

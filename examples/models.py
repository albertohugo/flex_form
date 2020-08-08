from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    HARDCOVER = 1
    PAPERBACK = 2
    EBOOK = 3
    BOOK_TYPES = (
        (HARDCOVER, 'Hardcover'),
        (PAPERBACK, 'Paperback'),
        (EBOOK, 'E-book'),
    )
    title = models.CharField(max_length=50)
    publication_date = models.DateField(null=True)
    author = models.CharField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pages = models.IntegerField(blank=True, null=True)
    book_type = models.PositiveSmallIntegerField(choices=BOOK_TYPES)

    timestamp = models.DateField(auto_now_add=True, auto_now=False)

class Form(models.Model):
    title = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    timestamp = models.DateField(auto_now_add=True, auto_now=False)

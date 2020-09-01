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
    status = models.BooleanField(default=True)
    private = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    timestamp = models.DateField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title


class FormMember(models.Model):
    ADMIN = 1
    MEMBER = 2
    OBJECT_TYPES = (
        (ADMIN, 'Admin'),
        (MEMBER, 'Member'),
    )
    form = models.ForeignKey('form', related_name='member', on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=OBJECT_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    def __str__(self):
        if self.user is not None:
            return str(self.user.username) + ':' + str(self.role)
        else:
            return ''

class Object(models.Model):
    STRING = 1
    NUMBER = 2
    OBJECT_TYPES = (
        (STRING, 'String'),
        (NUMBER, 'Number'),
    )
    form = models.ForeignKey('form', related_name='object', on_delete=models.CASCADE)
    label = models.CharField(max_length=50)
    description = models.CharField(max_length=100, default="",  blank = True)
    type = models.PositiveSmallIntegerField(choices=OBJECT_TYPES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    timestamp = models.DateField(auto_now_add=True, auto_now=False)
    def __str__(self):
        return self.label

class IdResult(models.Model):
    form = models.ForeignKey('form', related_name='response', on_delete=models.CASCADE)

    def __str__(self):
        if self.id is not None:
            return str(self.id)
        else:
            return ''

class Result(models.Model):
    form = models.ForeignKey('form', on_delete=models.CASCADE)
    object = models.ForeignKey('object', on_delete=models.CASCADE)
    id_result = models.ForeignKey('idresult', related_name='response_detail', on_delete=models.CASCADE)
    value = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    timestamp = models.DateField(auto_now_add=True, auto_now=False)
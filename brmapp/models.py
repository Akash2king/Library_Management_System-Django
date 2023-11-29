from django.db import models

# Create your models here.


class Book(models.Model):
    title=models.CharField(max_length=50)
    author=models.CharField(max_length=50)
    no_of_copies=models.IntegerField()
    book_no=models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    def __str__(self):
        return self.title
# book_management/models.py


class Student(models.Model):

    name = models.CharField(max_length=100)
    reg_number = models.CharField(max_length=20)
    department = models.CharField(max_length=50,default='IT')
    ph_no = models.IntegerField()

    def __str__(self):
        return self.name


# -*- coding: UTF-8 -*-
from django.db import models
# django.db.models def all kinds of operations of database, thus it become very easy to use 


class User(models.Model):
    account = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20)
    passwd = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)


class Book(models.Model):
    isbn = models.BigIntegerField(max_length=13, primary_key=True)
    bookname = models.CharField(max_length=50)
    number = models.IntegerField()
    authorname = models.CharField(max_length=50)
    booktype = models.CharField(max_length=50)
    callnumber = models.CharField(max_length=20)
    publisher = models.CharField(max_length=50)
    puclishtime = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Borrow(models.Model):
    account = models.ForeignKey(User)
    isbn = models.ForeignKey(Book)
    begintime = models.DateTimeField()
    endtime = models.DateTimeField()
    realtime = models.DateTimeField()
    add = models.IntegerField(default=0)


class OnlineUser(models.Model):
    account = models.ForeignKey(User)


class Fine(models.Model):
    account = models.ForeignKey(User)
    fine = models.DecimalField(max_digits=10, decimal_places=2)
    dealtime = models.DateField()

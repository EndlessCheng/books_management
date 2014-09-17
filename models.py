from django.db import models 
# django.db.models def all kinds of operations of database, thus it become very easy to use 

# just def the member variable in each class
class User(models.Model):
	account = models.CharField(max_length = 20, primary_key = True)
	name = models.CharField(max_length = 20)
	passwd = models.CharField(max_length = 20)
	email = models.EmailField(max_length = 50)
	
class Book(models.Model):
	isbn = models.IntegerField(max_length = 13, primary_key = True)
	bookname = models.CharField(max_length = 50)
	number = models.IntegerField()
	authorname = models.CharField(max_length = 50)
	booktype = models.CharField(max_length = 50)
	callnumber = models.CharField(max_length = 20)
	publisher = models.CharField(max_length = 50)
	puclishtime = models.DateField()
	price = models.DecimalField(max_digits = 10, decimal_places = 2)
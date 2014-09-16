from django.db import models

# define your class here

class People(models.Model):
	email = models.EmailField(primary_key=True)
	name = models.CharField(max_length = 30)
	sex = models.BooleanField(default = True)

class User(models.Model):
	email = models.EmailField(max_length = 50, primary_key = True)
	name = models.CharField(max_length = 40)
	passwd = models.IntegerField()
	
class Book(models.Model):
	isbn = models.IntegerField(max_length = 13, primary_key = True)
	bookname = models.CharField(max_length = 100)
	authorname = models.CharField(max_length = 100)
	publisher = models.CharField(max_length = 100)
	puclishtime = models.DateField()
	price = models.DoubleField() # 大小限制？

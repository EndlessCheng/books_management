from django.db import models

class People(models.Model):
	name = models.CharField(max_length = 30)
	sex = models.BooleanField(default = True)
	email = models.EmailField()
	

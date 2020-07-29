from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):

	user=models.OneToOneField(User,on_delete=models.CASCADE)
	uid=models.CharField(max_length=10,default='#')
	branch=models.CharField(max_length=4,default='#')
	year=models.CharField(max_length=2,default='#')
	sem=models.CharField(max_length=1,default='#')


	def __str__ (self):

		return "{} {}".format(self.user.first_name,self.user.last_name)
 
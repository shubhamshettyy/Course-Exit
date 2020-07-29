from django.db import models
from django.contrib.auth.models import User
from student.models import Student
from django.shortcuts import reverse
# Create your models here.


class Course(models.Model):
	cname=models.CharField(max_length=100)
	branch=models.CharField(max_length=4)
	year=models.CharField(max_length=2)
	sem=models.CharField(max_length=1)

	def __str__ (self):

		return "{}".format(self.cname) 


class Question(models.Model):

	course=models.ForeignKey(Course,on_delete=models.CASCADE)
	question=models.CharField(max_length=255)

	def __str__ (self):

		return "{} - {}".format(self.course.cname,self.question)

	def get_absolute_url(self):
		return reverse('show_questions',kwargs={'id':self.course.id})

class Response(models.Model):

	question=models.ForeignKey(Question,on_delete=models.CASCADE)
	student=models.ForeignKey(Student,models.CASCADE)
	answer=models.CharField(max_length=255)

	def __str__ (self):

		return "{} - {}".format(self.student.user.first_name+" "+self.student.user.last_name,self.question.course.cname)

class CourseExitStatus(models.Model):

	course=models.ForeignKey(Course,on_delete=models.CASCADE)
	student=models.ForeignKey(Student,on_delete=models.CASCADE)
	status=models.CharField(max_length=10,default="Not Filled")

	def __str__ (self):

		return "{} - {}".format(self.student.user.first_name+" "+self.student.user.last_name,self.course.cname)

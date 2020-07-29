from django.db import models
from django.contrib.auth.models import User
from course.models import Course
# Create your models here.


class Teacher(models.Model):

	user = models.OneToOneField(User,on_delete=models.CASCADE)
	fid=models.CharField(max_length=10,default="#")

	def __str__(self):

		return "{} {}".format(self.user.first_name,self.user.last_name)

class FacultyCourseMapping(models.Model):

	teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
	course=models.ForeignKey(Course,on_delete=models.CASCADE)

	def __str__ (self):

		return "{} {} - {}".format(self.teacher.user.first_name,self.teacher.user.last_name,self.course.cname) 

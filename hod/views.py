from django.shortcuts import render

from teacher.models import FacultyCourseMapping,Teacher
from.models import Hod
from course.models import Question, Course, Response, CourseExitStatus
from django.contrib.auth.decorators import login_required

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


def home(request):

	if len(Hod.objects.filter(user=request.user))!=0:

		return render(request,'hod/hodhome.html',context={'SE':'SE','TE':'TE','BE':'BE','MTECH':'MTECH',})

	print('hello')

	return render(request,'student/forbidden.html')

def show_courses(request,year):

	if len(Hod.objects.filter(user=request.user))!=0:

		courses = Course.objects.filter(year=year)

		return render(request,'hod/show_courses.html',context={'courses':courses})

	print('hello')

	return render(request,'student/forbidden.html')
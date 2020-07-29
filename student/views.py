from django.shortcuts import render,redirect
from course.models import Course,Question,Response,CourseExitStatus
from .models import Student
from hod.models import Hod
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):

	if len(Student.objects.filter(user=request.user))!=0:
		sem = request.user.student.sem
		context ={
			'course':Course.objects.filter(sem=sem)
		}

		return render(request,'student/home.html',context=context)

	return render(request,'student/forbidden.html')

def redirectingview(request):

	if len(Student.objects.filter(user=request.user))!=0:
		
		return redirect('student-home')

	if len(Hod.objects.filter(user=request.user))!=0:
		return redirect('hod-home')

	return redirect('teacher-home')

@login_required
def show_questions(request,id):


	course_obj = Course.objects.filter(id=id).first()
	student = Student.objects.filter(user = request.user).first()
	course_exit_status_objects = CourseExitStatus.objects.filter(course=course_obj,student=student)

	if len(course_exit_status_objects)!=0:
		return render(request,'student/already_submitted.html')


	questions = Question.objects.filter(course=course_obj)
	index = [(i+1) for i in range(len(questions))]
	questions_with_index = list(zip(index,questions))
	flag = True

	if request.method == 'POST':

		for index,question in questions_with_index:
			answer = str(request.POST.get(str(index),""))

			if answer == '':
				flag = False

		if flag:

			for index,question in questions_with_index:
				answer = str(request.POST.get(str(index),""))

				response_obj = Response(question=question,student=student,answer=answer)
				response_obj.save()

			course_exit_status_obj = CourseExitStatus(course=course_obj,student=student,status="Filled")
			course_exit_status_obj.save()
			messages.success(request,f'Your Response has been recorded!')
			return redirect('student-home')
		else:
			messages.warning(request,f'Please, Answer all the questions!')

	# print(questions_with_index[0])

	context = {
			'questions':questions_with_index
		}

	return render(request,'student/show_questions.html',context=context)

@login_required
def change_password(request):

	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST,user=request.user)

		if form.is_valid():
			form.save()
			update_session_auth_hash(request,form.user)
			messages.success(request,f'Your Password has been changed!')
			return redirect('redirectingurl')

		else:
			messages.warning(request,f'Your form is invalid!')
			return redirect('changepassword')

	form = PasswordChangeForm(user=request.user)
	context = {'form':form}
	return render(request,'student/change_password.html',context)
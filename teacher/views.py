from django.shortcuts import render
from .models import FacultyCourseMapping,Teacher
from hod.models import Hod
from course.models import Question, Course, Response, CourseExitStatus
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

@login_required
def home(request):

	if len(Teacher.objects.filter(user=request.user))!=0:
		context ={
			'faculty_course_mappings': FacultyCourseMapping.objects.filter(teacher = request.user.teacher)
		}

		return render(request,'teacher/home.html',context=context)

	return render(request,'student/forbidden.html')

@login_required
def show_questions(request,id):
	isTeacher = len(Teacher.objects.filter(user=request.user))!=0
	isHod = len(Hod.objects.filter(user=request.user))!=0

	if isTeacher or isHod:

		course_obj = Course.objects.filter(id=id).first() 

		Questions = Question.objects.filter(course=course_obj)

		context = {'questions':Questions,'course':course_obj,'isHod':not isHod}

		return render(request,'teacher/show_questions.html',context)

	return render(request,'student/forbidden.html')	

@login_required
def show_responses(request,id,pk):
	if len(Teacher.objects.filter(user=request.user))!=0 or len(Hod.objects.filter(user=request.user))!=0:

		course_obj = Course.objects.filter(id=id).first()

		question_obj = Question.objects.filter(course=course_obj).filter(id=pk).first()

		responses = Response.objects.filter(question=question_obj)
		labels = ['Average','High','Low']
		data = [len(Response.objects.filter(question=question_obj).filter(answer='Average')), len(Response.objects.filter(question=question_obj).filter(
			answer='High')), len(Response.objects.filter(question=question_obj).filter(answer='Low'))]

		context = {'responses': responses, 'labels_list': labels,
                    'data_list': data, 'question': question_obj.question}

		return render(request,'teacher/show_responses.html',context) 

	return render(request,'student/forbidden.html')


class QuestionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model=Question	
	fields=['question']

	def form_valid(self,form):
		course_obj = Course.objects.filter(id=self.kwargs['id']).first()
		form.instance.course = course_obj
		return super().form_valid(form)

	def test_func(self):

		course_obj = Course.objects.filter(id=self.kwargs['id']).first()
		faculty_course_mappings = FacultyCourseMapping.objects.filter(course = course_obj)

		for faculty_course_mapping in faculty_course_mappings:
			if self.request.user == faculty_course_mapping.teacher.user:
				return True

		return False

class QuestionUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
	model=Question	
	fields=['question']

	def form_valid(self,form):
		course_obj = Course.objects.filter(id=self.kwargs['id']).first()
		form.instance.course = course_obj
		return super().form_valid(form)

	def test_func(self):

		course_obj = Course.objects.filter(id=self.kwargs['id']).first()
		faculty_course_mappings = FacultyCourseMapping.objects.filter(course = course_obj)

		for faculty_course_mapping in faculty_course_mappings:
			if self.request.user == faculty_course_mapping.teacher.user:
				return True

		return False	

class QuestionDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
	model=Question
	success_url=''

	def test_func(self):

		self.success_url = '/teacher/course/{}/questions'.format(self.kwargs['id'])

		course_obj = Course.objects.filter(id=self.kwargs['id']).first()
		faculty_course_mappings = FacultyCourseMapping.objects.filter(course = course_obj)

		for faculty_course_mapping in faculty_course_mappings:
			if self.request.user == faculty_course_mapping.teacher.user:
				return True

		return False			

def download_pdf(request,id):

	course_obj = Course.objects.filter(id=id).first()
	course_exit_status_objects = CourseExitStatus.objects.filter(course=course_obj)

	question_objects = Question.objects.filter(course=course_obj)

	all_students_responses = []

	for course_exit_status_object in course_exit_status_objects:

		one_student_response = []

		for question_object in question_objects:

			response_obj = Response.objects.filter(question = question_object,student = course_exit_status_object.student).first()

			one_student_response.append((course_exit_status_object.student,question_object.question,response_obj.answer))

		all_students_responses.append(one_student_response)

	print(all_students_responses)

	html_string = render_to_string('teacher/download.html', {'all_students_responses':all_students_responses})

	html = HTML(string=html_string,base_url=request.build_absolute_uri())
	fs = FileSystemStorage('./')
	print(fs.location)
	html.write_pdf(target='./mypdf.pdf');

	with fs.open('mypdf.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
		return response

	return response

def analysis_pdf(request,id):

	course_obj = Course.objects.filter(id=id).first()
	questions = Question.objects.filter(course=course_obj)

	analysis = []

	for question in questions:

		average = len(Response.objects.filter(question=question,answer='Average'))

		high = len(Response.objects.filter(question=question,answer='High'))

		low = len(Response.objects.filter(question=question,answer='Low'))

		total = average + high + low

		analysis.append((average,high,low,question,total))

	html_string = render_to_string('teacher/analysis.html', {'analysis':analysis,'course':course_obj})

	html = HTML(string=html_string,base_url=request.build_absolute_uri())
	fs = FileSystemStorage('./')
	print(fs.location)
	html.write_pdf(target='./mypdf.pdf');

	with fs.open('mypdf.pdf') as pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
		return response

	return response







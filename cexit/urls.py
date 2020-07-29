
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from student import views as student_views
from teacher import views as teacher_views
from hod import views as hod_views
from teacher.views import QuestionCreateView,QuestionUpdateView,QuestionDeleteView
from course import views as course_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',auth_views.LoginView.as_view(template_name="student/login.html"),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name="student/logout.html"),name='logout'),

    path('student/home',student_views.home,name='student-home'),
    path('teacher/home',teacher_views.home,name='teacher-home'),
    path('hod/home',hod_views.home,name='hod-home'),

    path('redirectingurl',student_views.redirectingview,name='redirectingurl'),

    path('teacher/course/<int:id>/questions',teacher_views.show_questions,name='show_questions'),
    path('teacher/course/<int:id>/questions/create',QuestionCreateView.as_view(),name='create_questions'),
    path('teacher/course/<int:id>/questions/<int:pk>/update',QuestionUpdateView.as_view(),name='update_questions'),
    path('teacher/course/<int:id>/questions/<int:pk>/delete',QuestionDeleteView.as_view(),name='delete_questions'),
    path('teacher/course/<int:id>/questions/<int:pk>/responses',teacher_views.show_responses,name='show_responses'),

    path('student/course/<int:id>/questions',student_views.show_questions,name='show_questions_students'),

    path('hod/courses/<str:year>/',hod_views.show_courses,name="show_courses"),
    
    path('changepassword',student_views.change_password,name="changepassword"),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='course/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='course/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='course/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='course/password_reset_complete.html'
         ),
         name='password_reset_complete'),


    path('pdf/',course_views.html_to_pdf_view,name='pdf'),
    path('teacher/course/<int:id>/download',teacher_views.download_pdf,name='download-pdf'),
    path('teacher/course/<int:id>/analysis',teacher_views.analysis_pdf,name='analysis-pdf')

]
   
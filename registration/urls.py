from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns=[
    url('^register/$',memberRegistration),
    url(r'^loginuser',login),
    url(r'^logoutuser',logout),
    url(r'^addcourse',addcourse),
    url(r'^teachergetcourse',teachergetcourse),
    url(r'^getChapters',getChapters),
    url(r'^addChapter',addChapter),
    url(r'^getTopics',getTopics),
    url(r'^addTopic',addTopic),
    url(r'^getQuiz',getQuiz),
    url(r'^addQuiz',addQuiz),
    url(r'^getQuestions',getQuestions),
    url(r'^addQuestion',addQuestion),
    url(r'^usergetcourses', usergetcourses),
    url(r'^subscribeCourse', subscribeCourse),
    url(r'^getUserChapters',getUserChapters),
    url(r'^getUserTopics', getUserTopics),
    url(r'^getUserQuizs', getUserQuizs),
    url(r'^getuserallQuestions', getuserallQuestions),
    url(r'^submitQuiz', submitQuiz),
    url(r'^getscore', getscore)

]
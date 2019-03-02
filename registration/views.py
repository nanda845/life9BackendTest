import random
import string

from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import hashlib

# Create your views here.
from registration.models import userProfile, Token, CourseNames, Chapters, Topics, Quiz, Questions, QuizParticipants


def encrypt_password(password):
    encrypt = hashlib.md5(password.encode('utf-8')).hexdigest()
    print ("ghgjgjghjgjgjgjgj",encrypt)
    return encrypt

def authentication(tokennumber):
    try:
        token_object = Token.objects.get(token=tokennumber)
        return token_object.user
    except Exception as e:
        # print e
        return Response("Session Expired", status=status.HTTP_401_UNAUTHORIZED)

def random_number():
    chars = string.ascii_uppercase + string.digits
    randomnum = ''.join(random.choice(chars) for _ in range(50))
    check = Token.objects.filter(token=randomnum)
    if check:
        random_number()
    return randomnum


def token(tokennumber, profile):
    token_object = Token()
    token_object.token = tokennumber
    token_object.role = profile.role
    token_object.user = profile.id
    token_object.save()

@api_view(['POST'])
def memberRegistration(request):
    full_name = request.data['fullname']
    mobile_number = request.data['mobilenumber']
    password = request.data['password']
    role=request.data['role']
    try:
        user = User.objects.get(username=mobile_number)
        if user:
            return Response("User already exists", status=status.HTTP_200_OK)
    except User.DoesNotExist:
        try:
            print("i m inside")
            with transaction.atomic():
                print("hiiiiiiiiiiiiiii")
                user1=User()
                user1.username = mobile_number
                user1.password = encrypt_password(password)
                user1.last_name = ""
                user1.first_name = full_name
                user1.is_active = True
                user1.save()
                userid = User.objects.get(id=user1.id)
                print("mobile", userid)
                profile = userProfile()
                profile.user = userid
                profile.full_name = full_name
                profile.mobile_number = mobile_number
                profile.role=role
                profile.save()
            return Response("Registration success", status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Registration failed", status=status.HTTP_200_OK)



@api_view(['POST'])
def login(request):
    print("login---------",request.data)
    mobile = request.data['mobilenumber']
    password = encrypt_password(request.data['password'])
    user = User.objects.filter(username = mobile,password = password, is_active = True)
    if user:
        profile = userProfile.objects.filter(mobile_number = mobile)
        token_number = random_number()
        token(token_number, profile[0])
        data = {'role': profile[0].role,'user_id':profile[0].user_id, 'token': token_number}
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = {'role': 'mobile number or password wrong', 'token': 'error'}
        return Response(data)


@api_view(['POST'])
def logout(request):
    token_number = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    token_number.delete()
    return Response('loggedout', status=status.HTTP_200_OK)

@api_view(['POST'])
def addcourse(request):
    print("add course---------",request.data)
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    print ("inside -----------",id)
    crs=CourseNames()
    crs.teacher_id=id
    crs.name=request.data['courseName']
    crs.save()
    return Response("Success")


@api_view(['GET'])
def teachergetcourse(request):
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    crs=CourseNames.objects.filter(teacher_id=id).values()
    return Response(crs)


@api_view(['POST'])
def getChapters(request):
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    chap=Chapters.objects.filter(course_id=request.data['id']).values()
    return Response(chap)



@api_view(['POST'])
def addChapter(request):
    print("chap-----------------",request.data)
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    chap=Chapters()
    chap.chaptername=request.data['chapterName']
    chap.course_id=request.data['course_id']
    chap.save()
    return Response("success")


@api_view(['POST'])
def getTopics(request):
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    chap=Topics.objects.filter(chapter_id=request.data['id']).values()
    return Response(chap)



@api_view(['POST'])
def addTopic(request):
    print("topic-----------------",request.data)
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    chap=Topics()
    chap.topicName=request.data['topicName']
    chap.course_id=request.data['course_id']
    chap.chapter_id=request.data['chapter_id']
    chap.save()
    return Response("success")


@api_view(['POST'])
def getQuiz(request):
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    chap=Quiz.objects.filter(topic_id=request.data['id']).values()
    return Response(chap)



@api_view(['POST'])
def addQuiz(request):
    print("quiz-----------------",request.data)
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    chap=Quiz()
    chap.quiz_name=request.data['quiz_name']
    chap.course_id=request.data['course_id']
    chap.chapter_id=request.data['chapter_id']
    chap.topic_id=request.data['topic_id']
    chap.save()
    return Response("success")


@api_view(['POST'])
def getQuestions(request):
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    chap=Questions.objects.filter(quiz_id=request.data['id']).values()
    return Response(chap)



@api_view(['POST'])
def addQuestion(request):
    print("quiz-----------------",request.data)
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    chap=Questions()
    chap.quiz_id=request.data['quiz_id']
    chap.topic_id=request.data['topic_id']
    chap.question=request.data['question']
    chap.opt_a=request.data['A']
    chap.opt_b=request.data['B']
    chap.opt_c=request.data['C']
    chap.opt_d=request.data['D']
    chap.answer=request.data['answer']
    chap.save()
    return Response("success")



@api_view(['GET'])
def usergetcourses(request):
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    crs=CourseNames.objects.filter().values()
    return Response(crs)



@api_view(['POST'])
def subscribeCourse(request):
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    chap=CourseNames.objects.filter(id=request.data['id']).values()
    a=chap[0]['subscribeIds']
    if id in chap[0]['subscribeIds']:
        pass
    else:
        print("inside else-------------------")
        a.append(id)
        CourseNames.objects.filter(id=request.data['id']).update(subscribeIds=a)
    return Response("Success")



@api_view(['POST'])
def getUserChapters(request):
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    chap=Chapters.objects.filter(course_id=request.data['id']).values()
    return Response(chap)


@api_view(['POST'])
def getUserTopics(request):
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    chap=Topics.objects.filter(chapter_id=request.data['id']).values()
    return Response(chap)


@api_view(['POST'])
def getUserQuizs(request):
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    chap=Quiz.objects.filter(topic_id=request.data['id']).values()
    return Response(chap)



@api_view(['POST'])
def getuserallQuestions(request):
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    chap=Questions.objects.filter(quiz_id=request.data['id']).values()
    return Response(chap)


@api_view(['POST'])
def submitQuiz(request):
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    print("with 0=================",request.data[0], len(request.data))
    print("all ans------------",request.data)
    a=request.data
    score=0
    quiz_id=''
    for i in a:
        print ("inside for -------",i['id'])
        chap = Questions.objects.get(id=i['id'])
        quiz_id=chap.quiz_id
        print("anaaaaaaaaaaaa------",chap.question)
        if i['selectedanswer'].upper()==chap.answer:
            score+=1
        else:
            pass
    a=Quiz.objects.filter(id=quiz_id).values()
    ab=a[0]['participateIds']
    if id in a[0]['participateIds']:
        pass
    else:
        print("inside else-------------------")
        ab.append(id)
        Quiz.objects.filter(id=quiz_id).update(participateIds=ab)

        qp=QuizParticipants()
        qp.participant_id=id
        qp.Quiz_id=quiz_id
        qp.score=score
        qp.total=len(request.data)
        qp.save()
    # chap=Questions.objects.filter(id=request.data['id']).values()
    return Response(score)



@api_view(['POST'])
def getscore(request):
    id = authentication(request.META['HTTP_AUTHORIZATION'])
    chap=QuizParticipants.objects.filter(Quiz_id=request.data['id'],participant_id=id).values()
    return Response(chap)
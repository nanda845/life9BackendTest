from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
class userProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    full_name = models.TextField(max_length=100, null=True, blank=True)
    mobile_number = models.TextField(unique=True, null=True, blank=True)
    role = models.TextField()


class CourseNames(models.Model):
    name=models.TextField(max_length=150,null=True)
    teacher_id=models.IntegerField()
    subscribeIds=ArrayField(models.IntegerField(blank=True),default=list)


class Chapters(models.Model):
    chaptername=models.TextField()
    course_id=models.IntegerField()


class Topics(models.Model):
    topicName=models.TextField()
    chapter_id=models.IntegerField()
    course_id=models.IntegerField(null=True)


class Quiz(models.Model):
    topic_id =models.IntegerField()
    chapter_id=models.IntegerField()
    course_id=models.IntegerField(null=True)
    quiz_name=models.TextField()
    participateIds=ArrayField(models.IntegerField(blank=True),default=list)


class Questions(models.Model):
    quiz_id=models.IntegerField()
    topic_id = models.IntegerField()
    question=models.TextField()
    opt_a=models.CharField(max_length=150)
    opt_b=models.CharField(max_length=150)
    opt_c=models.CharField(max_length=150)
    opt_d=models.CharField(max_length=150)
    answer=models.CharField(max_length=150)

class QuizParticipants(models.Model):
    participant_id=models.IntegerField()
    Quiz_id=models.IntegerField()
    score=models.IntegerField()
    total=models.IntegerField()


class Token(models.Model):
    token = models.CharField(max_length=50, null=True, blank=True)
    user = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)
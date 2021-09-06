from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from random import randint
from django.contrib.postgres.fields import ArrayField
from django_jalali.db import models as jmodels



# class Participant(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
#     firstname = models.CharField(max_length=200)
#     lastname = models.CharField(max_length=200)
#     phone_number = models.CharField(unique=True,max_length=50,null=True)
#     mellicode = models.CharField(unique=True,max_length=10,validators=[MinLengthValidator(10)])
#     SEMAT_CHOICES = (
#         ('Ostad','Ostad'),
#         ('daneshamoz','daneshamoz'),
#     )
#     semat = models.CharField(max_length=200 ,choices=SEMAT_CHOICES ,default = 'daneshamoz')
#     def __str__(self):
#         return self.mellicode

def random_address():
    final = ''
    li = 'abcdefghijklmnopqrstuxwzy1234567890'
    for i in range(10):
        random_index = randint(1,34)
        final += li[random_index]
    return final

class Class(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, default=random_address())
    participant_number = models.IntegerField(default=0)
    azmoon_number = models.IntegerField(default=0)
    owner = models.IntegerField(null = True)
    def __str__(self):
        return self.name

class Azmoon(models.Model):
    azmoonclass = ManyToManyField(Class,blank=True)
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField(blank=True,null=True)
    end_time = models.DateTimeField(blank=True,null=True)
    Question_number = models.IntegerField(default=0)
    isactive = models.BooleanField(default=False)
    showable = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Participant(AbstractUser):
    partclass = models.ManyToManyField(Class,blank=True)
    azmoon = models.ManyToManyField(Azmoon,blank=True)
    phone_number = models.CharField(unique=True,max_length=50,null=True)
    mellicode = models.CharField(unique=True,max_length=10,validators=[MinLengthValidator(10)])
    def __str__(self):
        return self.mellicode

class Part_class(models.Model):
    participant = models.ForeignKey(Participant,blank=True,on_delete=models.CASCADE)
    partclass = models.ForeignKey(Class,blank=True,null=True,on_delete=models.CASCADE)
    SEMAT_CHOICES = (
        ('Ostad','Ostad'),
        ('daneshamoz','daneshamoz'),
    )
    semat = models.CharField(max_length=200 ,choices=SEMAT_CHOICES ,default = 'daneshamoz')

class Examiner(models.Model):
    participant = models.ForeignKey(Participant,blank=True,on_delete=models.CASCADE)
    partclass = models.ForeignKey(Class,blank=True,null=True,on_delete=models.CASCADE)
    azmoon = models.ForeignKey(Azmoon,blank=True,on_delete=models.CASCADE)
    percent_score = models.FloatField(default = 0,blank=True)
    score = models.FloatField(default = 0,blank=True)
    rank = models.IntegerField(default = 0,blank=True)
    end_time = models.DateTimeField(blank=True,null=True)


class Question(models.Model):
    azmoon = models.ManyToManyField(Azmoon,blank=True)
    Q_text = models.TextField()
    Q_image = models.ImageField(
            upload_to='questions_image',
            default = 'questions_image/8.jpeg'
        )
    TYPE_CHOICES = (
        ('goz','chand gozineh ee'),
        ('tash','tashrihi'),
    )
    ANSWER_CJOICES = (
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
    )
    answer1 = models.CharField(max_length=200,null = True, default="گزینه 1")
    answer2 = models.CharField(max_length=200,null = True, default="گزینه 2")
    answer3 = models.CharField(max_length=200,null = True, default="گزینه 3")
    answer4 = models.CharField(max_length=200,null = True, default="گزینه 4")

    correct_answer = models.CharField(max_length=1,choices=ANSWER_CJOICES,null = True)

    def __str__(self):
        return "Question " + str(self.id)

class Answer(models.Model):
    examiner = models.ForeignKey(Examiner,blank=True,null=True,on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant,blank=True,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,blank=True,on_delete=models.CASCADE)
    ANSWER_CJOICES = (
        ('', '---Please select your choice---'),
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
    )
    answer = models.CharField(max_length=200,choices=ANSWER_CJOICES,null=True)
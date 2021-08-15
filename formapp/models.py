from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

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

class Participant(AbstractUser):
    phone_number = models.CharField(unique=True,max_length=50,null=True)
    mellicode = models.CharField(unique=True,max_length=10,validators=[MinLengthValidator(10)])
    SEMAT_CHOICES = (
        ('Ostad','Ostad'),
        ('daneshamoz','daneshamoz'),
    )
    semat = models.CharField(max_length=200 ,choices=SEMAT_CHOICES ,default = 'daneshamoz')
    def __str__(self):
        return self.mellicode

class Azmoon(models.Model):
    participant = ManyToManyField(Participant,blank=True)
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField(blank=True,null=True)
    end_time = models.DateTimeField(blank=True,null=True)
    Question_number = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Question(models.Model):
    azmoon = models.ManyToManyField(Azmoon,blank=True)
    Q_text = models.TextField()
    Q_image = models.ImageField(blank=True)
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
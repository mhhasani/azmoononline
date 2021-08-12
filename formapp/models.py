from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class Participant(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
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
    Q_text = models.TextField(blank=True)
    Q_image = models.ImageField(blank=True)
    TYPE_CHOICES = (
        ('goz','chand gozineh ee'),
        ('tash','tashrihi'),
    )
    type = models.CharField(choices=TYPE_CHOICES , max_length=20,blank=True,null=True)
    def set_azmoon(self,id):
        self.azmoon__id = id
        self.save()
        return id
    def __str__(self):
        return "Question " + str(self.id)
from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.fields.related import ManyToManyField

class Participant(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    mellicode = models.CharField(unique=True,max_length=10,validators=[MinLengthValidator(10)])
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
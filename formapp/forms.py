from django.forms.fields import CharField
from .models import *
from django import forms

class AzmoonForm(forms.ModelForm):
    class Meta:
        model = Azmoon
        fields = ('name', 'start_time','end_time')

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('Q_text', 'Q_image','type')

class QuestionForm2(forms.Form):
    Q_text = CharField(widget=forms.Textarea,required=False)
    Q_image = forms.ImageField(required=False)
    TYPE_CHOICES = (
        ('goz','chand gozineh ee'),
        ('tash','tashrihi'),
    )
    type = forms.ChoiceField(choices=TYPE_CHOICES)

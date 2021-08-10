from .models import *
from django import forms

class AzmoonForm(forms.ModelForm):
    class Meta:
        model = Azmoon
        fields = ('name', 'start_time','end_time','Question_number')

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('Q_text', 'Q_image','type')
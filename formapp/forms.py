from django.contrib.auth.forms import UserCreationForm
from django.forms.fields import ChoiceField
from django.forms.models import ModelMultipleChoiceField
from .models import *
from django import forms
from django.core.validators import MinLengthValidator

# class ParticipantForm(forms.ModelForm):
#     class Meta:
#         model = Participant
#         fields = ('__all__')

class SignUpForm(UserCreationForm):
    class Meta:
        # from django.contrib.auth import get_user_model
        # User = get_user_model()
        # model = User
        model = Participant
        fields = ('username','first_name','last_name','phone_number','mellicode','semat','password1', 'password2')

    def clean(self):
        cd = self.cleaned_data
        u = Participant.objects.all()
        for part in u:
            if part.username == cd.get('username'):
                self.add_error('username', "username is requiered !")     
            if part.phone_number == cd.get('phone_number'):
                self.add_error('phone_number', "phone number is requiered !")
            if part.mellicode == cd.get('mellicode'):
                self.add_error('mellicode', "melli code is requiered !")
        return cd

class AzmoonForm2(forms.Form):
    participant = ModelMultipleChoiceField(Participant.objects,required=False)
    name = forms.CharField()
    start_time = forms.DateTimeField(required=False)
    end_time = forms.DateTimeField(required=False)

# class AzmoonForm(forms.ModelForm):
#     class Meta:
#         model = Azmoon
#         fields = ('name', 'start_time','end_time')
        
class QuestionForm(forms.Form):
    # azmoon = ModelMultipleChoiceField(Azmoon.objects,required=False)
    Q_text = forms.CharField(widget=forms.Textarea,required=True)
    Q_image = forms.ImageField(required=False)
    answer1 = forms.CharField(initial="گزینه 1",required=False)
    answer2 = forms.CharField(initial="گزینه 2",required=False)
    answer3 = forms.CharField(initial="گزینه 3",required=False)
    answer4 = forms.CharField(initial="گزینه 4",required=False)
    ANSWER_CJOICES = (
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
    )
    correct_answer = ChoiceField(choices=ANSWER_CJOICES)
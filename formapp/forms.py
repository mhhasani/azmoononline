from django.contrib.auth.forms import UserCreationForm
from django.forms.fields import ChoiceField
from .models import *
from django import forms
from django.core.validators import MinLengthValidator

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('__all__')

class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=11)
    mellicode = forms.CharField(max_length=10,validators=[MinLengthValidator(10)])
    SEMAT_CHOICES = (
        ('Ostad','Ostad'),
        ('daneshamoz','daneshamoz'),
    )
    semat = forms.ChoiceField(choices=SEMAT_CHOICES)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','phone_number','mellicode','semat','password1', 'password2')

    def clean(self):
        cd = self.cleaned_data
        u = Participant.objects.all()
        Us = User.objects.all()
        for user in Us:
            if user.username == cd.get('username'):
                self.add_error('username', "username is requiered !")     
        for part in u:
            if part.phone_number == cd.get('phone_number'):
                self.add_error('phone_number', "phone number is requiered !")
            if part.mellicode == cd.get('mellicode'):
                self.add_error('mellicode', "melli code is requiered !")
        return cd

    def save(self, commit=True):
        user = super().save(commit=commit)
        Participant.objects.create(
            user = user,
            firstname =self.cleaned_data['first_name'],
            lastname =self.cleaned_data['last_name'],
            phone_number=self.cleaned_data['phone_number'],
            mellicode=self.cleaned_data['mellicode'],
            semat=self.cleaned_data['semat'],
            )
        return user

class AzmoonForm(forms.ModelForm):
    class Meta:
        model = Azmoon
        fields = ('name', 'start_time','end_time')

class QuestionForm(forms.Form):
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
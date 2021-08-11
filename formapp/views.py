from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def Home(request):
    azmoons = Azmoon.objects.all()
    for azmoon in azmoons:
        q = Question.objects.all().filter(azmoon__id=azmoon.id)
        azmoon.Question_number = q.count()
        azmoon.save()
    context = {'azmoon':azmoons}
    return render(request, 'Home.html',context=context)
    
def show_participant(request,id):
    participant = Participant.objects.all().get(id=id)
    azmoon = Azmoon.objects.all().filter(participant__id = id)
    context = {'participant':participant , 'azmoon':azmoon}
    return render(request, 'show_participant.html', context=context)

def show_azmoon(request):
    azmoons = Azmoon.objects.all()
    for azmoon in azmoons:
        q = Question.objects.all().filter(azmoon__id=azmoon.id)
        azmoon.Question_number = q.count()
        azmoon.save()
    context = {'azmoon':azmoons}
    return render(request, 'show_azmoon.html', context=context)

def show_questions(request,id):
    questions = Question.objects.all()
    azmoon = Azmoon.objects.get(id=id)
    context = {'questions':questions,'id':id,'azmoon':azmoon}
    return render(request, 'show_question.html', context=context)

def add_azmoon(request):
    if request.method == "GET":
        form = AzmoonForm()
        return render(request, 'add_azmoon.html', {'form': form})
    if request.method == "POST":
        form = AzmoonForm(request.POST)
        azmoons = Azmoon.objects.all()
        context = {'azmoons':azmoons,'form': form}
        if form.is_valid():
            azmoon = form.save()  
            return render(request, 'add_azmoon_2.html', context=context)  
        else:
            return render(request, 'add_azmoon.html' ,context=context)       

def add_question(request,id):
    azmoon = Azmoon.objects.filter(id=id)
    azmoon2 = Azmoon.objects.get(id=id)
    if request.method == "GET":
        form = QuestionForm2()
        context = {'form': form,'id':id,'azmoon':azmoon2}
        return render(request, 'add_question.html', context=context)
    if request.method == "POST":
        form = QuestionForm2(request.POST)
        context = {'form': form,'id':id,'azmoon':azmoon2}
        if form.is_valid():
            question = Question.objects.create()
            question.Q_text = form.cleaned_data['Q_text']
            question.Q_image = form.cleaned_data['Q_image']
            question.type = form.cleaned_data['type']
            question.azmoon.set(azmoon)
            question.save()
            return render(request, 'add_question_2.html', context=context)  
        else:
            return render(request, 'add_question.html' ,context=context)   

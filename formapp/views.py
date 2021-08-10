from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import *
from .models import *
from django.views.generic import CreateView

def Home(request):
    return render(request, 'Home.html')
    
def show_participant(request,id):
    participant = Participant.objects.all().get(id=id)
    azmoon = Azmoon.objects.all().filter(participant__id = id)
    context = {'participant':participant , 'azmoon':azmoon}
    return render(request, 'show_participant.html', context=context)

def show_azmoon(request):
    azmoons = Azmoon.objects.all()
    context = {'azmoons':azmoons}
    return render(request, 'show_azmoon.html', context=context)

def show_questions(request,id):
    questions = Question.objects.all()
    context = {'questions':questions,'id':id}
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
    azmoon = Azmoon.objects.all()
    if request.method == "GET":
        form = QuestionForm()
        context = {'form': form,'id':id,'azmoon':azmoon}
        return render(request, 'add_question.html', {'form': form})
    if request.method == "POST":
        form = QuestionForm(request.POST)
        context = {'form': form,'id':id,'azmoon':azmoon}
        if form.is_valid(): 
            question = form.save()
            return render(request, 'add_question_2.html', context=context)  
        else:
            return render(request, 'add_question.html' ,context=context)   

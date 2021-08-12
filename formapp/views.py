from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

@csrf_exempt
def signup(request):
    if request.method == 'GET':
        form = SignUpForm()
        context = {'form': form}
        return render(request, 'registration/signup.html', context=context)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return HttpResponse(f"{form.errors}") 

def Home(request):
    return render(request, 'Home.html')
    
@login_required
def show_participant(request,id):
    participant = Participant.objects.all().get(id=id)
    azmoon = Azmoon.objects.all().filter(participant__id = id)
    context = {'participant':participant , 'azmoon':azmoon , 'id':id}
    return render(request, 'show_participant.html', context=context)

@login_required
def show_azmoon(request):
    azmoons = Azmoon.objects.all()
    for azmoon in azmoons:
        q = Question.objects.all().filter(azmoon__id=azmoon.id)
        azmoon.Question_number = q.count()
        azmoon.save()
    context = {'azmoon':azmoons}
    return render(request, 'show_azmoon.html', context=context)

@login_required
def show_questions(request,id):
    questions = Question.objects.all()
    azmoon = Azmoon.objects.get(id=id)
    user = User.objects.all()
    context = {'questions':questions,'id':id,'azmoon':azmoon,'user':user}
    return render(request, 'show_question.html', context=context)

@login_required
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
            return redirect('azmoon')
        else:
            return render(request, 'add_azmoon.html' ,context=context)       

@login_required
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
            question.answer1 = form.cleaned_data['answer1']
            question.answer2 = form.cleaned_data['answer2']
            question.answer3 = form.cleaned_data['answer3']
            question.answer4 = form.cleaned_data['answer4']
            question.correct_answer = form.cleaned_data['correct_answer']
            question.azmoon.set(azmoon)
            question.save()
            return redirect('quest',id)
        else:
            return render(request, 'add_question.html' ,context=context)   

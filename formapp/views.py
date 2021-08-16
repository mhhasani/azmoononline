from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from openpyxl import Workbook


@csrf_exempt
def signup(request):
    if request.method == 'GET':
        form = SignUpForm()
        context = {'form': form}
        return render(request, 'registration/signup.html', context=context)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'registration/signup.html', context=context)

def Home(request):
    return render(request, 'Home.html')

def Profile(request):
    participant = request.user
    if request.method == "GET":
        form = ProfileForm(
            initial = 
            {
                'username' : participant.username,
                'first_name' : participant.first_name,
                'last_name' : participant.last_name,
                'phone_number' : participant.phone_number,
                'mellicode' : participant.mellicode,
                'semat' : participant.semat,
            }
        )
        context = {'form': form,'participant':participant}
        return render(request, 'registration/Profile.html', context=context)
    if request.method == "POST":
        form = ProfileForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            participant.username = form.cleaned_data['username']
            participant.first_name = form.cleaned_data['first_name']
            participant.last_name = form.cleaned_data['last_name']
            participant.phone_number = form.cleaned_data['phone_number']
            participant.mellicode = form.cleaned_data['mellicode']
            participant.save()
            return redirect('Home')
        else:
            return render(request, 'registration/Profile.html',context=context) 

def check_semat(user):
    if user.semat=="Ostad":
        return True

# @user_passes_test(check_semat)
@login_required
def show_participant(request,id):
    participant = Participant.objects.all().get(id=id)
    classes = Class.objects.all()
    context = {'participant':participant , 'classes':classes , 'id':id}
    return render(request, 'show_participant.html', context=context)

@login_required
def show_class(request):
    participant = Participant.objects.all().get(mellicode=request.user)
    for Class in participant.partclass.all():
        part = Participant.objects.all().filter(partclass__id = Class.id)
        az = Azmoon.objects.all().filter(azmoonclass__id = Class.id)
        Class.participant_number = part.count()
        Class.azmoon_number = az.count()
        Class.save()
    context = {'participant':participant}
    return render(request, 'show_class.html', context=context)

@login_required
def show_azmoon(request,id):
    participant = Participant.objects.all().get(mellicode=request.user)
    check_in_class = False
    for c in request.user.partclass.all():
        if c.id == id:
            check_in_class = True
            break
    if check_in_class:
        for azmoon in participant.azmoon.all():
            q = Question.objects.all().filter(azmoon__id=azmoon.id)
            azmoon.Question_number = q.count()
            azmoon.save()
        azmoon=[]
        for az in participant.azmoon.all():
            for b in az.azmoonclass.all():
                if id == b.id:
                    azmoon.append(az)
                    break 
        context = {'participant':participant,'id':id,'azmoon':azmoon}
        return render(request, 'show_azmoon.html', context=context)
    else:
        return HttpResponse("کلاس یافت نشد")

@login_required
def show_questions(request,id):
    question = Question.objects.all().filter(azmoon__id=id).values()
    participant = Participant.objects.all().filter(azmoon__id=id).values()
    azmoons = Azmoon.objects.all() 
    check_in_azmoon = False
    for azmoon in request.user.azmoon.all():
        if azmoon.id == id:
            check_in_azmoon = True
            break
    if check_in_azmoon:
        wb = Workbook()
        ws = wb.active
        ws.title = "Data"
        ws.append(['id','firstname','lastname','phone_number','mellicode','semat'])
        for part in participant:
            ws.append([part['id'],part['first_name'],part['last_name'],part['phone_number'],part['mellicode'],part['semat']])
        wb.save(f"azmoon_{id}_participant.xlsx")
        context = {'questions':question,'id':id,'participant':participant}
        return render(request, 'show_question.html', context=context)
    else:
        return HttpResponse("آزمون یافت نشد")

    
# @login_required
# def add_azmoon(request):
#     if request.method == "GET":
#         form = AzmoonForm()
#         return render(request, 'add_azmoon.html', {'form': form})
#     if request.method == "POST":
#         form = AzmoonForm(request.POST)
#         azmoons = Azmoon.objects.all()
#         context = {'azmoons':azmoons,'form': form}
#         if form.is_valid():
#             azmoon = form.save()  
#             return redirect('azmoon')
#         else:
#             return render(request, 'add_azmoon.html' ,context=context)       

# @user_passes_test(check_semat)

@login_required
def add_azmoon2(request,id):
    cls = Class.objects.all().get(id=id)
    participant = Participant.objects.all().get(mellicode=request.user)
    if request.method == "GET":
        form = AzmoonForm2()
        return render(request, 'add_azmoon.html', {'form': form})
    if request.method == "POST":
        form = AzmoonForm2(request.POST)
        azmoons = Azmoon.objects.all()
        context = {'azmoons':azmoons,'form': form,'id':id}
        if form.is_valid():
            azmoon = Azmoon.objects.create() 
            azmoon.name = form.cleaned_data['name']                       
            azmoon.start_time = form.cleaned_data['start_time']                       
            azmoon.end_time = form.cleaned_data['end_time'] 
            azmoon.azmoonclass.add(cls)
            azmoon.save()  
            participant.azmoon.add(azmoon)                
            return redirect('azmoon',id)
        else:
            return render(request, 'add_azmoon.html' ,context=context) 
            
@login_required
def add_question(request,id):
    azmoon = Azmoon.objects.filter(id=id)
    azmoon2 = Azmoon.objects.get(id=id)
    if request.method == "GET":
        form = QuestionForm()
        context = {'form': form,'id':id,'azmoon':azmoon2}
        return render(request, 'add_question.html', context=context)
    if request.method == "POST":
        form = QuestionForm(request.POST)
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

@login_required
def edit_question(request,q_id,a_id):
    azmoon = Azmoon.objects.all().get(id=a_id)
    question = Question.objects.all().get(id=q_id)
    if request.method == "GET":
        form = QuestionForm(
            initial = 
            {
                # 'azmoon' : question.azmoon,
                'Q_text' : question.Q_text,
                'Q_image' : question.Q_image,
                'answer1' : question.answer1,
                'answer2' : question.answer2,
                'answer3' : question.answer3,
                'answer4' : question.answer4,
                'correct_answer' : question.correct_answer
            }
        )
        context = {'form': form,'id':q_id,'azmoon':azmoon}
        return render(request, 'edit_question.html', context=context)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        context = {'form': form,'id':q_id,'azmoon':azmoon}
        if form.is_valid():
            question.Q_text = form.cleaned_data['Q_text']
            question.Q_image = form.cleaned_data['Q_image']
            question.answer1 = form.cleaned_data['answer1']
            question.answer2 = form.cleaned_data['answer2']
            question.answer3 = form.cleaned_data['answer3']
            question.answer4 = form.cleaned_data['answer4']
            question.correct_answer = form.cleaned_data['correct_answer']
            # question.azmoon.set(form.cleaned_data['azmoon'])
            question.save()
            return redirect('quest',a_id)
        else:
            return render(request, 'edit_question.html' ,context=context) 
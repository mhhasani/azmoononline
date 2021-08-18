from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from openpyxl import Workbook
from django.shortcuts import get_object_or_404


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
    for azmoon in participant.azmoon.all():
        q = Question.objects.all().filter(azmoon__id=azmoon.id)
        azmoon.Question_number = q.count()
        azmoon.save()
    context = {'participant':participant}
    return render(request, 'show_class.html', context=context)

@login_required
def search_class(request):
    participant = Participant.objects.all().get(mellicode=request.user)
    if request.method == "GET":
        form = JoinClassForm()
        return render(request, 'search_class.html', {'form': form})        
    if request.method == "POST":
        form = JoinClassForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            cls = get_object_or_404(Class,address = form.cleaned_data['join_code'])
            # cls = Class.objects.all().get(address = form.cleaned_data['join_code'])
            return redirect('join_class',cls.address)
        else:
            return HttpResponse("کلاس یافت نشد")

@login_required
def join_class(request,join_code):
    cls = get_object_or_404(Class,address = join_code)
    participant = Participant.objects.all().get(mellicode=request.user)
    if cls:
        participant.partclass.add(cls)
        return redirect('class')        
    else:
        return HttpResponse("کلاس یافت نشد")

@login_required
def show_azmoon(request,id):
    participant = Participant.objects.all().get(mellicode=request.user)
    participants = Participant.objects.all().filter(partclass__id=id).values()
    az = Azmoon.objects.all().filter(azmoonclass__id=id).values()
    check_in_class = False
    for c in request.user.partclass.all():
        if c.id == id:
            check_in_class = True
            break
    if check_in_class:
        for azmoon in az:
            q = Question.objects.all().filter(azmoon__id=azmoon['id'])
            azmoon['Question_number'] = q.count()
        azmoon=[]
        for a in az:
            azmoon.append(a)
        cls = Class.objects.all().get(id=id)
        context = {'participants':participants,'id':id,'azmoon':azmoon,'class':cls}
        return render(request, 'show_azmoon.html', context=context)
    else:
        return HttpResponse("کلاس یافت نشد")

@login_required
def show_questions(request,id):
    question = Question.objects.all().filter(azmoon__id=id).values()
    participant = Participant.objects.all().get(mellicode = request.user)
    # azmoon = Azmoon.objects.all().get(id=id)
    azmoon = get_object_or_404(Azmoon, id=id)
    check_in_class = False
    for clsp in participant.partclass.all():
        for clsa in azmoon.azmoonclass.all():
            if clsp.id == clsa.id:
                check_in_class = True
                break
    if check_in_class:
        # wb = Workbook()
        # ws = wb.active
        # ws.title = "Data"
        # ws.append(['id','firstname','lastname','phone_number','mellicode'])
        # for part in participant:
        #     ws.append([part['id'],part['first_name'],part['last_name'],part['phone_number'],part['mellicode']])
        # wb.save(f"azmoon_{id}_participant.xlsx")
        context = {'questions':question,'id':id}
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
    az = Azmoon.objects.all().filter(azmoonclass__id = id).values()
    azid = []
    for azmoon in az:
        azid.append(azmoon['id'])
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
            for a in azid:
                A = Azmoon.objects.all().get(id=a)
                A.azmoonclass.add(cls) 
            return redirect('azmoon',id)
        else:
            return render(request, 'add_azmoon.html' ,context=context) 

@login_required
def add_class(request):
    participant = Participant.objects.all().get(mellicode=request.user)
    if request.method == "GET":
        form = ClassForm()
        return render(request, 'add_class.html', {'form': form})
    if request.method == "POST":
        form = ClassForm(request.POST)
        clas = Class.objects.all()
        context = {'class':clas,'form': form}
        if form.is_valid():
            Cls = Class.objects.create() 
            Cls.name = form.cleaned_data['name']                       
            participant.partclass.add(Cls)  
            Cls.owner = participant.id
            Cls.save()  
            return redirect('class')
        else:
            return render(request, 'add_class.html' ,context=context) 

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
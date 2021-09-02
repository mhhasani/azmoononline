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
            # participant.username = form.cleaned_data['username']
            participant.first_name = form.cleaned_data['first_name']
            participant.last_name = form.cleaned_data['last_name']
            # participant.phone_number = form.cleaned_data['phone_number']
            # participant.mellicode = form.cleaned_data['mellicode']
            participant.save()
            return redirect('Home')
        else:
            return render(request, 'registration/Profile.html',context=context) 

@login_required
def show_participant(request,id):
    user = Participant.objects.all().get(mellicode=request.user)
    part = get_object_or_404(Participant, id=id)
    check_in_class = False
    for classes in user.partclass.all():
        for cls in part.partclass.all():
            if classes.id == cls.id:
                check_in_class = True
                break
        if check_in_class:
            break
    if check_in_class:
        classes = Class.objects.all()
        context = {'participant':part , 'classes':classes , 'id':id}
        return render(request, 'show_participant.html', context=context)
    else:
        return HttpResponse("کاربر مورد نظر یافت نشد")

@login_required
def show_class(request):
    participant = Participant.objects.all().get(mellicode=request.user)
    pc = Part_class.objects.all().filter(participant=participant)
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
    context = {'participant':participant,'pc':pc}
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
    cls = Class.objects.all().get(id=id)
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
        pc = Part_class.objects.all().filter(participant = participant).filter(partclass__id=id)
        if not pc:
            p_class = Part_class.objects.create(
                participant = participant,
                partclass = cls
            )

            if cls.owner == participant.id:
                p_class.semat = "Ostad"
            else:
                p_class.semat = "daneshamoz"
            p_class.save() 
        wb = Workbook()
        ws = wb.active
        ws.title = "Data"
        ws.append(['id','firstname','lastname','phone_number','mellicode'])
        for part in participants:
            ws.append([part['id'],part['first_name'],part['last_name'],part['phone_number'],part['mellicode']])
        wb.save(f"class_{id}_participant.xlsx")
        pc = Part_class.objects.all().filter(partclass__id=id)
        context = {'participants':participants,'id':id,'azmoon':azmoon,'class':cls,'pc':pc}
        return render(request, 'show_azmoon.html', context=context)
    else:
        return HttpResponse("کلاس یافت نشد")

@login_required
def show_questions(request,id):
    question = Question.objects.all().filter(azmoon__id=id).values()
    participant = Participant.objects.all().get(mellicode = request.user)
    azmoon = get_object_or_404(Azmoon, id=id)
    check_in_class = False
    for clsp in participant.partclass.all():
        for clsa in azmoon.azmoonclass.all():
            if clsp.id == clsa.id:
                check_in_class = True
                break
    if check_in_class:        
        context = {'questions':question,'id':id,'azmoon':azmoon}
        return render(request, 'show_question.html', context=context)
    else:
        return HttpResponse("آزمون یافت نشد")

@login_required
def add_azmoon2(request,id):
    user = Participant.objects.all().get(mellicode=request.user)
    cls = get_object_or_404(Class, id=id)
    check_in_class = False
    for classes in user.partclass.all():
        if classes.id == id:
                check_in_class = True
                break
        if check_in_class:
            break
    if check_in_class:
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
    else:
        return HttpResponse("کلاس مورد نظر یافت نشد")

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
    question = Question.objects.all().filter(azmoon__id=id).values()
    participant = Participant.objects.all().get(mellicode = request.user)
    # azmoon = Azmoon.objects.all().get(id=id)
    azmoon = get_object_or_404(Azmoon, id=id)
    check_in_azmoon = False
    for classes in participant.partclass.all():
        for azmoons in azmoon.azmoonclass.all():
            if classes.id == azmoons.id:
                check_in_azmoon = True
                break
        if check_in_azmoon:
            break
    if check_in_azmoon:
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
    else:
        return HttpResponse("آزمون مورد نظر یافت نشد")

@login_required
def edit_question(request,q_id,a_id):
    question = Question.objects.all().filter(azmoon__id=q_id).values()
    participant = Participant.objects.all().get(mellicode = request.user)
    # azmoon = Azmoon.objects.all().get(id=id)
    azmoon = get_object_or_404(Azmoon, id=a_id)
    check_in_azmoon = False
    for classes in participant.partclass.all():
        for azmoons in azmoon.azmoonclass.all():
            if classes.id == azmoons.id:
                check_in_azmoon = True
                break
        if check_in_azmoon:
            break
    if check_in_azmoon:
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
    else:
        return HttpResponse("سوال مورد نظر یافت نشد")

@login_required
def edit_class(request,id):
    participant = Participant.objects.all().get(mellicode = request.user)
    # azmoon = Azmoon.objects.all().get(id=id)
    cls = get_object_or_404(Class, id=id)
    check_in_class = False
    for classes in participant.partclass.all():
        if classes.id == id:
            check_in_class = True
            break
    if check_in_class:
        cls = Class.objects.all().get(id=id)
        if request.method == "GET":
            form = ClassForm(
                initial = 
                {
                    'name' : cls.name,
                }
            )
            context = {'form': form,'id':id}
            return render(request, 'edit_class.html', context=context)
        if request.method == "POST":
            form = ClassForm(request.POST)
            context = {'form': form,'id':id}
            if form.is_valid():
                cls.name = form.cleaned_data['name']
                cls.save()
                return redirect('azmoon',id)
            else:
                return render(request, 'edit_class.html' ,context=context) 
    else:
        return HttpResponse("کلاس مورد نظر یافت نشد")

@login_required
def edit_azmoon(request,id):
    participant = Participant.objects.all().get(mellicode = request.user)
    # azmoon = Azmoon.objects.all().get(id=id)
    azmoon = get_object_or_404(Azmoon, id=id)
    check_in_azmoon = False
    for classes in participant.partclass.all():
        for azmoons in azmoon.azmoonclass.all():
            if classes.id == azmoons.id:
                check_in_azmoon = True
                break
        if check_in_azmoon:
            break
    if check_in_azmoon:
        azmoon = Azmoon.objects.all().get(id=id)
        if request.method == "GET":
            form = AzmoonForm2(
                initial = 
                {
                    'name' : azmoon.name,
                    'start_time' : azmoon.start_time,
                    'end_time' : azmoon.end_time,
                }
            )
            context = {'form': form,'id':id}
            return render(request, 'edit_azmoon.html', context=context)
        if request.method == "POST":
            form = AzmoonForm2(request.POST)
            context = {'form': form,'id':id}
            if form.is_valid():
                azmoon.name = form.cleaned_data['name']
                azmoon.start_time = form.cleaned_data['start_time']
                azmoon.end_time = form.cleaned_data['end_time']
                azmoon.save()
                return redirect('quest',id)
            else:
                return render(request, 'edit_azmoon.html' ,context=context) 
    else:
        return HttpResponse("آزمون مورد نظر یافت نشد")

@login_required
def activate_azmoon(request,id):
    participant = Participant.objects.all().get(mellicode = request.user)
    azmoon = get_object_or_404(Azmoon, id=id)
    check_in_azmoon = False
    for classes in participant.partclass.all():
        for azmoons in azmoon.azmoonclass.all():
            if classes.id == azmoons.id:
                check_in_azmoon = True
                break
        if check_in_azmoon:
            break
    if check_in_azmoon:
        if azmoon.isactive:
            azmoon.isactive = False
            azmoon.save()
        else:
            azmoon.isactive = True
            azmoon.save() 
        return redirect('quest',id)
    else:
        return HttpResponse("آزمون مورد نظر یافت نشد")

@login_required
def showable_azmoon(request,id):
    participant = Participant.objects.all().get(mellicode = request.user)
    azmoon = get_object_or_404(Azmoon, id=id)
    check_in_azmoon = False
    for classes in participant.partclass.all():
        for azmoons in azmoon.azmoonclass.all():
            if classes.id == azmoons.id:
                check_in_azmoon = True
                break
        if check_in_azmoon:
            break
    if check_in_azmoon:
        if azmoon.showable:
            azmoon.showable = False
            azmoon.save()
        else:
            azmoon.showable = True
            azmoon.save() 
        return redirect('quest',id)
    else:
        return HttpResponse("آزمون مورد نظر یافت نشد")

@login_required         
def natijeh_azmoon(request,id):
    participant = Participant.objects.all().get(mellicode = request.user)
    question = Question.objects.all().filter(azmoon__id=id).values()
    azmoon = get_object_or_404(Azmoon, id=id)
    check_in_class = False
    for clsp in participant.partclass.all():
        for clsa in azmoon.azmoonclass.all():
            if clsp.id == clsa.id:
                check_in_class = True
                break
    if check_in_class:   
        examiners = Examiner.objects.all().filter(azmoon__id = id)
        tedad = len(examiners)
        context = {'id':id,'examiners':examiners,'questions':question,'azmoon':azmoon,'tedad':tedad}
        return render(request, 'natijeh_azmoon.html',context=context) 
    else:
        return HttpResponse("آزمون مورد نظر یافت نشد")        

@login_required
def change_semat(request,id):
    participant = Participant.objects.all().get(mellicode = request.user)
    pc = get_object_or_404(Part_class, id=id)
    check_in_class = False
    for cls in participant.partclass.all():
        if pc.partclass.id == cls.id:
            check_in_class = True
            break
    if check_in_class:
        if pc.semat=="Ostad":
            pc.semat = "daneshamoz"
            pc.save()
        else:
            pc.semat = "Ostad"
            pc.save()
        return redirect('azmoon',pc.partclass.id)
    else:
        return HttpResponse("کاربر مورد نظر یافت نشد")

@login_required
def azmoon(request,id):
    question = Question.objects.all().filter(azmoon__id=id).values()
    participant = Participant.objects.all().get(mellicode = request.user)
    azmoon = get_object_or_404(Azmoon, id=id)
    check_in_class = False
    for clsp in participant.partclass.all():
        for clsa in azmoon.azmoonclass.all():
            if clsp.id == clsa.id:
                check_in_class = True
                break
    if check_in_class:
        examiner = Examiner.objects.all().filter(participant = participant).filter(azmoon=azmoon)
        if not examiner:
            exam = Examiner.objects.create(
                participant = participant,
                azmoon = azmoon,
            )
            exam.save() 
        examiner = Examiner.objects.all().filter(azmoon__id=id)          
        context = {'questions':question,'id':id,'azmoon':azmoon}
        if not azmoon.isactive:
            return HttpResponse("آزمون هنوز شروع نشده است!")            
        return render(request, 'azmoon.html', context=context)
    else:
        return HttpResponse("آزمون یافت نشد")
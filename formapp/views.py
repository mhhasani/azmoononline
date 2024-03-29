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
from django.forms import formset_factory
from django.utils import timezone
from datetime import timedelta

def check_is_ostad(participant,cls):
    part = get_object_or_404(Part_class,participant=participant,partclass=cls)
    if part.semat=="Ostad":
        return True
    else:
        return False

def convert_time_to_js(time,plus=None):
    if plus:
        time = time + plus
    date = str(time.month) + " " + str(time.day) + ", " + str(time.year) +" "+ str(time.hour) + ":" + str(time.minute) + ":" + str(time.second)
    return date

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
    user = Participant.objects.all().filter(mellicode=request.user)
    if not user:
        return render(request, 'Home.html')
    return redirect('Dashboard')

@login_required
def Dashboard(request):
    participant = Participant.objects.all().get(mellicode=request.user)
    classes_object = []
    all_azmoon = []
    for cls in participant.partclass.all():
        cls = Class.objects.all().get(id = cls.id)
        azmoon = Azmoon.objects.all().filter(azmoonclass = cls)
        for az in azmoon:
            az = Azmoon.objects.all().get(id = az.id)
            q = Question.objects.all().filter(azmoon__id=az.id)
            az.Question_number = q.count()
            az.save()
            if az.start_time>timezone.now() or (az.end_time>timezone.now() and az.start_time<timezone.now()):
                date = convert_time_to_js(az.start_time,timedelta(hours=4, minutes=30))
                now = convert_time_to_js(timezone.now())
                end = convert_time_to_js(az.end_time,timedelta(hours=4, minutes=30))
                all_azmoon.append([cls,az,az.start_time,check_is_ostad(participant,cls),date,now,end])
        classes_object.append(cls)
    all_azmoon = sorted(all_azmoon, key=lambda x: x[2])
    if all_azmoon != []:
        all_azmoon = [all_azmoon[0]]
    timenow=timezone.now()

    context = {'participant':participant,'azmoon':all_azmoon,'classes':classes_object,'timenow':timenow}
    return render(request, 'Dashboard.html',context=context)

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
        Pc = Part_class.objects.all().filter(participant = participant).filter(partclass = Class)
        if not Pc:
            p_class = Part_class.objects.create(
                participant = participant,
                partclass = Class
            )
            if Class.owner == participant.id:
                p_class.semat = "Ostad"
            else:
                p_class.semat = "daneshamoz"
            p_class.save() 
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
    cls = get_object_or_404(Class,id=id)
    az = Azmoon.objects.all().filter(azmoonclass__id=id).values()
    check_in_class = False
    for c in request.user.partclass.all():
        if c.id == id:
            check_in_class = True
            break
    if check_in_class:
        for azmoon in az:
            q = Question.objects.all().filter(azmoon__id=azmoon['id'])
            a = Azmoon.objects.all().get(id = azmoon['id'])
            a.Question_number = q.count()
            a.save()
            azmoon['Question_number'] = q.count()
        azmoon=[]
        for a in az:
            a = Azmoon.objects.all().get(id = a['id'])
            date = convert_time_to_js(a.start_time,timedelta(hours=4, minutes=30))
            now = convert_time_to_js(timezone.now())
            end = convert_time_to_js(a.end_time,timedelta(hours=4, minutes=30))
            azmoon.append([a,date,now,end])
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
        now = timezone.now()
        context = {'participants':participants,'id':id,'azmoon':azmoon,'class':cls,'pc':pc,'participant':participant,'check_is_ostad':check_is_ostad(participant,cls),'timenow':now}
        return render(request, 'show_azmoon.html', context=context)
    else:
        return HttpResponse("کلاس یافت نشد")

@login_required
def show_questions(request,id):
    question = Question.objects.all().filter(azmoon__id=id).values()
    participant = Participant.objects.all().get(mellicode = request.user)
    azmoon = get_object_or_404(Azmoon, id=id)
    date = convert_time_to_js(azmoon.start_time,timedelta(hours=4, minutes=30))
    now = convert_time_to_js(timezone.now())
    end = convert_time_to_js(azmoon.end_time,timedelta(hours=4, minutes=30))
    print(now,date)
    examiner = Examiner.objects.all().filter(participant=participant,azmoon=azmoon)
    if examiner:
        examiner = Examiner.objects.all().get(participant=participant,azmoon=azmoon)
    check_in_class = False
    cls = None
    for clsp in participant.partclass.all():
        for clsa in azmoon.azmoonclass.all():
            if clsp.id == clsa.id:
                cls = Class.objects.all().get(id=clsp.id)
                check_in_class = True
                break
    if check_in_class:        
        context = {'questions':question,'id':id,'azmoon':azmoon,'check_is_ostad':check_is_ostad(participant,cls),'class':cls,'examiner':examiner,'date':date,'now':now,'end':end}
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
    if check_is_ostad(user,cls):
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
                    azmoon = Azmoon.objects.create(
                        name = form.cleaned_data['name'],                       
                        start_time = form.cleaned_data['start_time'],                       
                        end_time = form.cleaned_data['end_time'],
                    ) 
                    azmoon.azmoonclass.add(cls)
                    azmoon.save()
                    for a in azid:
                        A = Azmoon.objects.all().get(id=a)
                        A.azmoonclass.add(cls) 
                    return redirect('quest',azmoon.id)
                else:
                    return render(request, 'add_azmoon.html' ,context=context) 
        else:
            return HttpResponse("کلاس مورد نظر یافت نشد")
    else:
        return HttpResponse("شما دسترسی لازم برای اضافه کردن آزمون به این کلاس را ندارید")

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
            return redirect('azmoon',Cls.id)
        else:
            return render(request, 'add_class.html' ,context=context) 

@login_required
def add_question(request,id):
    participant = Participant.objects.all().get(mellicode = request.user)
    azmoon = get_object_or_404(Azmoon, id=id)
    cls=None
    check_in_azmoon = False
    for classes in participant.partclass.all():
        for azmoons in azmoon.azmoonclass.all():
            if classes.id == azmoons.id:
                cls = Class.objects.all().get(id=classes.id)
                check_in_azmoon = True
                break
        if check_in_azmoon:
            break
    if check_is_ostad(participant,cls):
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
                    q = Question.objects.create()
                    q.Q_text = form.cleaned_data['Q_text']
                    q.Q_image = form.cleaned_data['Q_image']
                    q.answer1 = form.cleaned_data['answer1']
                    q.answer2 = form.cleaned_data['answer2']
                    q.answer3 = form.cleaned_data['answer3']
                    q.answer4 = form.cleaned_data['answer4']
                    q.correct_answer = form.cleaned_data['correct_answer']
                    q.azmoon.set(azmoon)
                    q.save()
                    return redirect('quest',id)
                else:
                    return render(request, 'add_question.html' ,context=context)   
        else:
            return HttpResponse("آزمون مورد نظر یافت نشد")
    else:
        return HttpResponse("شما دسترسی لازم برای اضافه کردن سوال به این آزمون را ندارید")

@login_required
def edit_question(request,q_id,a_id):
    question = Question.objects.all().filter(azmoon__id=q_id).values()
    participant = Participant.objects.all().get(mellicode = request.user)
    azmoon = get_object_or_404(Azmoon, id=a_id)
    check_in_azmoon = False
    cls=None
    for classes in participant.partclass.all():
        for azmoons in azmoon.azmoonclass.all():
            if classes.id == azmoons.id:
                cls = Class.objects.all().get(id=classes.id)
                check_in_azmoon = True
                break
        if check_in_azmoon:
            break
    if check_is_ostad(participant,cls):
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
    else:
        return HttpResponse("شما دسترسی لازم برای ویرایش سوالات این آزمون را ندارید")

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
    if check_is_ostad(participant,cls):
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
    else:
        return HttpResponse("شما دسترسی لازم برای ویرایش این کلاس را ندارید")

@login_required
def edit_azmoon(request,id):
    participant = Participant.objects.all().get(mellicode = request.user)
    # azmoon = Azmoon.objects.all().get(id=id)
    azmoon = get_object_or_404(Azmoon, id=id)
    check_in_azmoon = False
    cls = None
    for classes in participant.partclass.all():
        for azmoons in azmoon.azmoonclass.all():
            if classes.id == azmoons.id:
                check_in_azmoon = True
                cls = Class.objects.all().get(id=classes.id)     
                break
        if check_in_azmoon:
            break
    if check_is_ostad(participant,cls):
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
    else:
        return HttpResponse("شما دسترسی لازم برای ویرایش این آزمون را ندارید")

@login_required
def activate_natijeh(request,id):
    participant = Participant.objects.all().get(mellicode = request.user)
    azmoon = get_object_or_404(Azmoon, id=id)
    check_in_azmoon = False
    cls = None
    for classes in participant.partclass.all():
        for azmoons in azmoon.azmoonclass.all():
            if classes.id == azmoons.id:
                check_in_azmoon = True
                cls = Class.objects.all().get(id=classes.id)     
                break
        if check_in_azmoon:
            break
    if check_is_ostad(participant,cls):
        if check_in_azmoon:
            if azmoon.isactive_natijeh:
                azmoon.isactive_natijeh = False
                azmoon.save()
            else:
                azmoon.isactive_natijeh = True
                azmoon.save() 
            return redirect('quest',id)
        else:
            return HttpResponse("آزمون مورد نظر یافت نشد")
    else:
        return HttpResponse("شما دسترسی لازم برای فعالسازی نتیجه آزمون را ندارید")

@login_required
def activate_score_board(request,id):
    participant = Participant.objects.all().get(mellicode = request.user)
    azmoon = get_object_or_404(Azmoon, id=id)
    check_in_azmoon = False
    cls = None
    for classes in participant.partclass.all():
        for azmoons in azmoon.azmoonclass.all():
            if classes.id == azmoons.id:
                check_in_azmoon = True
                cls = Class.objects.all().get(id=classes.id)     
                break
        if check_in_azmoon:
            break
    if check_is_ostad(participant,cls):
        if check_in_azmoon:
            if azmoon.isactive_score_board:
                azmoon.isactive_score_board = False
                azmoon.save()
            else:
                azmoon.isactive_score_board = True
                azmoon.save() 
            return redirect('quest',id)
        else:
            return HttpResponse("آزمون مورد نظر یافت نشد")
    else:
        return HttpResponse("شما دسترسی لازم برای فعالسازی جدول امتیازات آزمون را ندارید")

@login_required
def showable_azmoon(request,id):
    participant = Participant.objects.all().get(mellicode = request.user)
    azmoon = get_object_or_404(Azmoon, id=id)
    check_in_azmoon = False
    cls = None
    for classes in participant.partclass.all():
        for azmoons in azmoon.azmoonclass.all():
            if classes.id == azmoons.id:
                check_in_azmoon = True
                cls = Class.objects.all().get(id=classes.id)     
                break
        if check_in_azmoon:
            break
    if check_is_ostad(participant,cls):
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
    else:
        return HttpResponse("شما دسترسی لازم برای آشکار کردن این آزمون را ندارید")

@login_required         
def score_board(request,id):
    participant = Participant.objects.all().get(mellicode = request.user)
    question = Question.objects.all().filter(azmoon__id=id).values()
    azmoon = get_object_or_404(Azmoon, id=id)
    check_in_class = False
    cls = None
    for clsp in participant.partclass.all():
        for clsa in azmoon.azmoonclass.all():
            if clsp.id == clsa.id:
                check_in_class = True
                cls = Class.objects.all().get(id=clsp.id)
                break
    pc = get_object_or_404(Part_class,participant=participant,partclass=cls)
    if check_in_class:
        if azmoon.isactive_score_board or check_is_ostad(participant,cls):   
            examiners = Examiner.objects.all().filter(azmoon__id = id)
            tedad = len(examiners)
            if question.count():
                for examiner in examiners:
                    sahih = 0
                    ghalat = 0
                    nazade = 0
                    an = Answer.objects.all().filter(examiner__id=examiner.id)
                    for answer in an:
                        if answer.answer == None:
                            nazade +=1
                        elif answer.answer == answer.question.correct_answer:
                            sahih +=1
                        else:
                            ghalat += 1
                    examiner.percent_score = ((3*sahih - ghalat)*100)/(3*(question.count()))
                    examiner.score = (sahih/question.count())*20
                    examiner.save()
                rank = 1
                for examiner1 in examiners:
                    for examiner2 in examiners:
                        if examiner2.percent_score>examiner1.percent_score:
                            rank+=1
                    examiner1.rank = rank 
                    examiner1.save()
                    rank = 1
                examiners = Examiner.objects.all().filter(azmoon__id = id).order_by('rank')
                context = {'id':id,'examiners':examiners,'questions':question,'azmoon':azmoon,'tedad':tedad,'pc':pc}
                return render(request, 'score_board.html',context=context)
            else:
                return HttpResponse("آزمون سوالی ندارد")        
        else:
            return HttpResponse("جدول امتیازات فعال نیست")        
    else:
        return HttpResponse("آزمون مورد نظر یافت نشد")        

@login_required         
def natijeh_azmoon(request,id):
    participant = Participant.objects.all().get(mellicode = request.user)
    examiner = Examiner.objects.all().filter(id=id)
    if not examiner:
        return HttpResponse("شما هنوز در آزمون شرکت نکرده اید")
    else:
        examiner = get_object_or_404(Examiner, id=id)
    azmoon = get_object_or_404(Azmoon, id=examiner.azmoon.id)
    question = Question.objects.all().filter(azmoon=azmoon).values()
    check_in_class = False
    cls=None
    for clsp in participant.partclass.all():
        for clsa in azmoon.azmoonclass.all():
            if clsp.id == clsa.id:
                check_in_class = True
                cls = Class.objects.all().get(id=clsp.id)
                break
    my_part_class = get_object_or_404(Part_class,participant=participant,partclass=cls)
    if check_in_class and (examiner.participant == participant or my_part_class.semat == "Ostad"):
        if azmoon.isactive_natijeh  or check_is_ostad(participant,cls):
            examiners = Examiner.objects.all().filter(azmoon = azmoon)
            if question.count():
                for examiner in examiners:
                    sahih = 0
                    ghalat = 0
                    nazade = 0
                    an = Answer.objects.all().filter(examiner__id=examiner.id)
                    for answer in an:
                        if answer.answer == None:
                            nazade +=1
                        elif answer.answer == answer.question.correct_answer:
                            sahih +=1
                        else:
                            ghalat += 1
                    examiner.percent_score = ((3*sahih - ghalat)*100)/(3*(question.count()))
                    examiner.score = (sahih/question.count())*20
                    examiner.save()
                rank = 1
                examiners = Examiner.objects.all().filter(azmoon = azmoon)
                for examiner1 in examiners:
                    for examiner2 in examiners:
                        if examiner2.percent_score>examiner1.percent_score:
                            rank+=1
                    examiner1.rank = rank 
                    examiner1.save()
                    rank = 1
                examiner = Examiner.objects.all().get(id = id)
                an = Answer.objects.all().filter(examiner__id=examiner.id)
                context = {'id':id,'examiner':examiner,'questions':question,'answers':an,'azmoon':azmoon}
                return render(request, 'natijeh_azmoon.html',context=context) 
            else:
                return HttpResponse("آزمون سوالی ندارد")
        else:
            return HttpResponse("نتیجه آزمون قابل مشاهده نیست")  
    else:
        return HttpResponse("دیدن نتیجه آزمون این کاربر برای شما مقدور نیست")  

@login_required
def change_semat(request,id):
    participant = Participant.objects.all().get(mellicode = request.user)
    pc = get_object_or_404(Part_class, id=id)
    check_in_class = False
    clsid = -1
    for cls in participant.partclass.all():        
        if pc.partclass.id == cls.id:
            check_in_class = True
            clsid = cls.id
            break
    if check_in_class:
        cls = Class.objects.all().get(id=clsid)
        if cls.owner==participant.id:
            if pc.participant.id == cls.owner:
                return HttpResponse("تغییر نقش مالک کلاس ممکن نیست")
            elif pc.semat=="Ostad":
                pc.semat = "daneshamoz"
                pc.save()
            else:
                pc.semat = "Ostad"
                pc.save()
            return redirect('azmoon',pc.partclass.id)
        else:
            return HttpResponse("شما دسترسی لازم برای تغییر نقش کاربران این کلاس را ندارید")        

    else:
        return HttpResponse("کاربر مورد نظر یافت نشد")  

@login_required
def azmoon(request,id):
    question = Question.objects.all().filter(azmoon__id=id).values()
    participant = Participant.objects.all().get(mellicode = request.user)
    finish_azmoon_all(request,id)
    azmoon = get_object_or_404(Azmoon, id=id)
    date = convert_time_to_js(azmoon.end_time,timedelta(hours=4, minutes=30))
    now = convert_time_to_js(timezone.now())
    length = question.count()
    if length:
        if (azmoon.showable) and ((azmoon.start_time<timezone.now() and azmoon.end_time > timezone.now())):
            examiner = Examiner.objects.all().filter(participant = participant).filter(azmoon=azmoon)
            check_in_class = False
            for clsp in participant.partclass.all():
                for clsa in azmoon.azmoonclass.all():
                    if clsp.id == clsa.id:
                        check_in_class = True
                        break
            qf =[]
            if check_in_class:
                if request.method == "GET":
                    QuestionFormSet = formset_factory(Azmoon_Form,extra=length)
                    QQ = QuestionFormSet()
                    if not examiner:
                        exam = Examiner.objects.create(
                            participant = participant,
                            azmoon = azmoon,
                        )
                        exam.save() 
                    exam = Examiner.objects.all().get(participant = participant,azmoon = azmoon)
                    if not exam.Finished:
                        for i in range(length):
                            Quest = Question.objects.all().get(id = question[i]['id'])
                            a = Answer.objects.all().filter(participant = participant,question = Quest , examiner__id=examiner.get().id)
                            if a:
                                c = Answer.objects.all().get(participant = participant,question = Quest, examiner=examiner.get())
                                c.examiner = examiner.get()
                                QQ[i]['answer'].initial = c.answer
                                c.save()
                            else:
                                answer = Answer.objects.create(
                                    participant = participant,
                                    question = Quest
                                )
                                answer.examiner = examiner.get()
                                answer.save()
                            qf.append([QQ[i],Quest])
                        q = Question.objects.all().filter(azmoon__id=azmoon.id)
                        a = Azmoon.objects.all().get(id = azmoon.id)
                        a.Question_number = q.count()
                        a.save()
                        azmoon.Question_number = q.count()
                        azmoon.save()
                        length = azmoon.Question_number
                        context = {'questions':question,'id':id,'azmoon':azmoon,'forms':QuestionFormSet,'Len':length,'qf':qf,'date':date,'now':now}  
                        return render(request, 'azmoon.html', context=context)
                    else:
                        return HttpResponse("شما قبلا آزمون را ثبت کرده اید!")
                if request.method == "POST":
                    QuestionFormSet = formset_factory(Azmoon_Form,extra=len(question))
                    QQ = QuestionFormSet(request.POST)
                    context = {'questions':question,'id':id,'azmoon':azmoon,'forms':QQ,'Len':length,'qf':qf,'date':date,'now':now}
                    c = examiner.get()
                    c.end_time = timezone.now()
                    c.save()
                    if QQ.is_valid() and not c.Finished:
                        for i in range(length):
                            cd = QQ[i].cleaned_data
                            Quest = Question.objects.all().get(id = question[i]['id'])
                            a = Answer.objects.all().filter(participant = participant,question = Quest , examiner__id=examiner.get().id)
                            c = Answer.objects.all().get(participant = participant,question = Quest, examiner=examiner.get())
                            c.answer = cd.get('answer')
                            c.examiner = examiner.get()
                            c.save()
                            qf.append([QQ[i],Quest])
                        return render(request, 'azmoon.html', context=context)
            else:
                return HttpResponse("آزمون یافت نشد")   
        elif azmoon.start_time > timezone.now() and azmoon.showable:
            return HttpResponse("آزمون هنوز شروع نشده است")
        elif azmoon.Finished:
            return HttpResponse("آزمون به پایان رسیده است")   
        else:
            return HttpResponse("آزمون غیر فعال است")  
    else: 
        return HttpResponse("آزمون بدون سوال است")  

# @login_required
# def finish_azmoon(request,id):
#     participant = Participant.objects.all().get(mellicode = request.user)
#     azmoon = get_object_or_404(Azmoon, id=id)
#     check_in_class = False
#     for cls in participant.partclass.all():
#         for az in azmoon.azmoonclass.all():
#             if cls.id == az.id:
#                 check_in_class = True
#                 break
#         if check_in_class:
#             break
#     if check_in_class:
#         examin = get_object_or_404(Examiner, azmoon=azmoon,participant=participant)
#         if examin.Finished==True:
#             return HttpResponse("شما قبلا آزمون را ثبت کرده اید!")
#         else:
#             examin.Finished=True
#             examin.save()
#             return redirect('quest',id)
#     else:
#         return HttpResponse("آزمون مورد نظر یافت نشد")

@login_required
def finish_azmoon_all(request,id):
    participant = Participant.objects.all().get(mellicode = request.user)
    azmoon = get_object_or_404(Azmoon, id=id)
    examiners = Examiner.objects.all().filter(azmoon=azmoon)
    check_in_class = False
    for cls in participant.partclass.all():
        for az in azmoon.azmoonclass.all():
            if cls.id == az.id:
                check_in_class = True
                break
        if check_in_class:
            break
    if check_in_class:
        if azmoon.end_time < timezone.now():
            azmoon.Finished=True
            azmoon.save()
            for examiner in examiners:
                examin = Examiner.objects.all().get(id = examiner.id)
                examin.Finished = True
                examin.save()
        else:
            azmoon.Finished=False
            azmoon.save()
            for examiner in examiners:
                examin = Examiner.objects.all().get(id = examiner.id)
                examin.Finished = False
                examin.save()

@login_required
def delete_class(request,id):
    participant = Participant.objects.all().get(mellicode=request.user)
    cls = get_object_or_404(Class,id=id) 
    if cls.owner == participant.id:
        for azmoon in Azmoon.objects.all():
            for clsa in azmoon.azmoonclass.all():
                if clsa.id == cls.id:
                    delete_azmoon(request,id,azmoon.id)
                    break
        for pc in Part_class.objects.all().filter(partclass = cls):
            p = Part_class.objects.all().get(id = pc.id)
            if p.partclass == cls:
                p.delete()       
        cls.delete()
        return redirect('class')
    else:
        return HttpResponse("شما دسترسی لازم برای حذف این کلاس را ندارید")

@login_required
def delete_azmoon(request,class_id,azmoon_id):
    participant = Participant.objects.all().get(mellicode=request.user)
    azmoon = get_object_or_404(Azmoon,id=azmoon_id)
    cls = get_object_or_404(Class,id = class_id)
    pc = get_object_or_404(Part_class,participant=participant,partclass=cls)
    if pc.semat == "Ostad":
        for examiner in Examiner.objects.all().filter(partclass = cls,azmoon=azmoon):
            examin = Examiner.objects.all().get(id = examiner['id'])
            for answer in Answer.objects.all().filter(examiner=examin):
                ans = Answer.objects.all().get(id = answer.id)
                ans.delete()
            examin.delete()
        for q in Question.objects.all().filter(azmoon=azmoon):
            delete_question(request,class_id,q.id)
        azmoon.delete()
        if Class.objects.all().filter(id = class_id):
            return redirect('azmoon',class_id)
        else:
            return redirect('class')
    else:
        return HttpResponse("شما دسترسی لازم برای حذف این آزمون را ندارید")

@login_required
def delete_question(request,class_id,question_id):
    participant = Participant.objects.all().get(mellicode=request.user)
    question = get_object_or_404(Question,id=question_id)
    cls = get_object_or_404(Class,id = class_id)
    pc = get_object_or_404(Part_class,participant=participant,partclass=cls)
    if pc.semat == "Ostad":
        for q in question.azmoon.all():
            if q.id:
                question.delete()
                return redirect("quest",q.id)
    else:
        return HttpResponse("شما دسترسی لازم برای حذف این سوال را ندارید")

def change_link_class(request,id):
    participant = Participant.objects.all().get(mellicode=request.user)
    cls = get_object_or_404(Class,id = id)
    pc = get_object_or_404(Part_class,participant=participant,partclass=cls)
    if pc.semat == "Ostad":
        cls.address = random_address()   
        cls.save()
        return redirect('azmoon',id)
    else:
        return HttpResponse("شما دسترسی لازم برای تغییر لینک این کلاس را ندارید")

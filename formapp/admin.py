from django.contrib import admin,messages
from .models import *
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

class AzmoonInline(admin.TabularInline):
    model = Azmoon.azmoonclass.through
    extra = 0

class ParticipantInline(admin.TabularInline):
    model = Participant.azmoon.through
    extra = 0

class Participant2Inline(admin.TabularInline):
    model = Participant.partclass.through
    extra = 0

class QuestionInline(admin.StackedInline):
    model = Question.azmoon.through
    extra = 0

class ClassInline(admin.StackedInline):
    model = Class
    extra = 0

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['id','name','address','participant_number','azmoon_number']
    inlines = [AzmoonInline,Participant2Inline]

@admin.register(Azmoon)
class AzmoonAdmin(admin.ModelAdmin):
    list_display = ['id','name','start_time','end_time','Question_number']
    inlines = [QuestionInline,ParticipantInline,AzmoonInline]

@admin.register(Question)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['id','correct_answer']
    inlines = [QuestionInline]

@admin.register(Participant)
class ParticipantAdmin(DefaultUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone_number',
                'mellicode',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = (
        'username',
        'first_name',
        'last_name',
        'phone_number',
        'is_staff',
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'phone_number',
        'email',
    )    
    inlines = [Participant2Inline,ParticipantInline]

@admin.register(Examiner)
class ExaminerAdmin(admin.ModelAdmin):
    list_display = ['id','participant','partclass','azmoon','percent_score','end_time']
    inlines = [AnswerInline]

@admin.register(Part_class)
class Part_classAdmin(admin.ModelAdmin):
    list_display = ['id','participant','partclass','semat']

@admin.register(Answer)
class SDAzmoonAdmin(admin.ModelAdmin):
    list_display = ['id','participant','question','answer']
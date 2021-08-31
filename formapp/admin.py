from django.contrib import admin,messages
from .models import *
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

class AzmoonInline(admin.TabularInline):
    model = Azmoon.azmoonclass.through

class ParticipantInline(admin.TabularInline):
    model = Participant.azmoon.through

class Participant2Inline(admin.TabularInline):
    model = Participant.partclass.through

class QuestionInline(admin.StackedInline):
    model = Question.azmoon.through

class ClassInline(admin.StackedInline):
    model = Class

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
    list_display = ['id','participant','partclass','azmoon','semat','percent_score']

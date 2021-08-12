from django.contrib import admin,messages
from .models import *
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Participant

class AzmoonInline(admin.TabularInline):
    model = Azmoon.participant.through

class QuestionInline(admin.StackedInline):
    model = Question.azmoon.through

@admin.register(Azmoon)
class AzmoonAdmin(admin.ModelAdmin):
    list_display = ['id','name','start_time','end_time','Question_number']
    inlines = [QuestionInline,AzmoonInline]

@admin.register(Question)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['id','correct_answer']
    inlines = [QuestionInline]

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['id','user','firstname','lastname','mellicode','semat']
    inlines = [AzmoonInline]


from django.contrib import admin,messages
from .models import *

class QuestionInline(admin.StackedInline):
    model = Question.azmoon.through

class AzmoonInline(admin.TabularInline):
    model = Azmoon.participant.through

@admin.register(Azmoon)
class AzmoonAdmin(admin.ModelAdmin):
    list_display = ['id','name','start_time','end_time','Question_number']
    inlines = [QuestionInline,AzmoonInline]

@admin.register(Question)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['id','type']
    inlines = [QuestionInline]

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['id','firstname','lastname','mellicode','semat']
    inlines = [AzmoonInline]


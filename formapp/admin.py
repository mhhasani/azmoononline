from django.contrib import admin,messages
from .models import *
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Participant

class ParticipantInline(admin.TabularInline):
    model = Participant.azmoon.through

class QuestionInline(admin.StackedInline):
    model = Question.azmoon.through

@admin.register(Azmoon)
class AzmoonAdmin(admin.ModelAdmin):
    list_display = ['id','name','start_time','end_time','Question_number']
    inlines = [QuestionInline,ParticipantInline]

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
                'semat',
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
        'semat',
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'phone_number',
        'email',
    )    
    inlines = [ParticipantInline]


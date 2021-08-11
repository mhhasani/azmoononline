from formapp.views import Home, show_participant,show_azmoon, show_questions,add_azmoon,add_question
from django.contrib import admin 
from django.urls import  path , include
from django.views.generic.base import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('show_azmoon/', show_azmoon,name='azmoon'),
    path('show_participant/<int:id>/',show_participant,name='part'),
    path('show_question/<int:id>/',show_questions,name='quest'),
    path('add_azmoon/',add_azmoon, name='add_azmoon'),
    path('add_question/<int:id>/',add_question, name='add_question'),
    path('accounts/', include('formapp.urls')),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('',TemplateView.as_view(template_name='Home.html'),name='Home'),
]

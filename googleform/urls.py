from formapp.views import edit_azmoon
from formapp.views import edit_class
from formapp.views import search_class , join_class
from formapp.views import add_class
from formapp.views import show_class
from formapp.views import Profile
from formapp.views import add_azmoon2
from formapp.views import Home, show_participant,show_azmoon, show_questions,add_question,edit_question,signup
from django.contrib import admin 
from django.urls import  path , include
from django.views.generic.base import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('show_azmoon/<int:id>/',show_azmoon,name='azmoon'),
    path('show_class/', show_class,name='class'),
    path('search/',search_class,name='search_class'),
    path('join/<str:join_code>',join_class,name='join_class'),
    path('show_participant/<int:id>/',show_participant,name='part'),
    path('show_question/<int:id>/',show_questions,name='quest'),
    path('add_azmoon/<int:id>/',add_azmoon2, name='add_azmoon'),
    path('add_class/',add_class, name='add_class'),
    path('add_question/<int:id>/',add_question, name='add_question'),
    path('edit_question/<int:q_id>/<int:a_id>/',edit_question, name='edit_question'),    
    path('edit_class/<int:id>/',edit_class, name='edit_class'),    
    path('edit_azmoon/<int:id>/',edit_azmoon, name='edit_azmoon'),    
    path('accounts/', include('formapp.urls')),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('Profile/', Profile , name = 'Profile'),
    path('',TemplateView.as_view(template_name='Home.html'),name='Home'),
]

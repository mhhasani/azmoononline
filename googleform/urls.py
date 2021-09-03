from formapp.views import azmoon
from formapp.views import showable_azmoon
from formapp.views import change_semat
from formapp.views import edit_azmoon
from formapp.views import edit_class
from formapp.views import search_class , join_class
from formapp.views import add_class
from formapp.views import show_class
from formapp.views import Profile
from formapp.views import add_azmoon2,natijeh_azmoon
from formapp.views import Home, show_participant,show_azmoon, show_questions,add_question,edit_question,signup,activate_azmoon
from django.contrib import admin 
from django.urls import path, include # new
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('show_azmoon/<int:id>/',show_azmoon,name='azmoon'),
    path('show_class/', show_class,name='class'),
    path('search/',search_class,name='search_class'),
    path('join/<str:join_code>',join_class,name='join_class'),
    path('show_participant/<int:id>/',show_participant,name='part'),
    path('show_question/<int:id>/',show_questions,name='quest'),
    path('add_azmoon/<int:id>/',add_azmoon2, name='add_azmoon'),
    path('natijeh_azmoon/<int:id>/',natijeh_azmoon, name='natijeh_azmoon'),
    path('add_class/',add_class, name='add_class'),
    path('add_question/<int:id>/',add_question, name='add_question'),
    path('edit_question/<int:q_id>/<int:a_id>/',edit_question, name='edit_question'),    
    path('edit_class/<int:id>/',edit_class, name='edit_class'),    
    path('edit_azmoon/<int:id>/',edit_azmoon, name='edit_azmoon'),    
    path('activate_azmoon/<int:id>/',activate_azmoon, name='activate_azmoon'),    
    path('azmoon/<int:id>/',azmoon, name='sherkat_dar_azmoon'),    
    path('showable_azmoon/<int:id>/',showable_azmoon, name='showable_azmoon'),    
    path('change_semat/<int:id>/',change_semat, name='change_semat'),    
    path('accounts/', include('formapp.urls')),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('Profile/', Profile , name = 'Profile'),
    path('',TemplateView.as_view(template_name='Home.html'),name='Home'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

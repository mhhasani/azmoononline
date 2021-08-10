"""googleform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from formapp.views import add_question
from formapp.views import add_azmoon
from formapp.views import Home, show_participant,show_azmoon, show_questions
from django.contrib import admin 
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('show_azmoon/', show_azmoon,name='azmoon'),
    path('show_participant/<int:id>/',show_participant,name='part'),
    path('show_question/<int:id>/',show_questions,name='quest'),
    path('add_azmoon/',add_azmoon, name='add_azmoon'),
    path('add_question/<int:id>/',add_question, name='add_question'),
    path('',Home,name='Home')
]

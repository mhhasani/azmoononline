from django.urls import path

from .views import show_azmoon, signup

urlpatterns = [
    path('signup/', signup, name='signup'),
]
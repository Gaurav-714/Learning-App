from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name = 'home'),
    path('course/<slug>', view_course, name = 'course'),
    path('become_pro/', become_pro, name = 'become_pro'),
    path('login/', login_page, name = 'login'),
    path('register/', register_page, name = 'register'),
]

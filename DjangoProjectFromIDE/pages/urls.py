from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_page, name='hello'),
    path('about/', views.about_page, name='about'),
]
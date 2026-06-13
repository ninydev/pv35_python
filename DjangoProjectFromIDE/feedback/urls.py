from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_page, name='feedback_page'),

]
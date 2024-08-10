# urls.py
from django.urls import path
from .views import licence_expiree

urlpatterns = [
    path('licence-expiree/', licence_expiree, name='licence_expiree'),
]
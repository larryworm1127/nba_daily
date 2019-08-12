"""Frontend App URL Mapping Module

@date: 08/09/2019
@author: Larry Shi
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
]

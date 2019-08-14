"""Frontend App Views Module

@date: 08/09/2019
@author: Larry Shi
"""
from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'frontend/index.html')

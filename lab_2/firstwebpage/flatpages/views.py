from django.shortcuts import render

# Create your views here.
from django import template

def home(request):
    return render(request, 'templates/static_handler.html')


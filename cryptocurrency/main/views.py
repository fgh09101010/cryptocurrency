from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def test_page(request):
    return render(request, 'test.html')
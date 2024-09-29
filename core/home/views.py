from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
    peoples = [
        {'name' : 'Arkoprovo' , 'age' : 23},
        {'name' : 'Rohan' , 'age' : 9},
        {'name' : 'Minu' , 'age' : 20}
    ]
    return render(request , "index.html" , context={'peoples' : peoples})

def contacts(request):
    return render(request , "contacts.html")

def about(request):
    return render(request , "about.html")

def success_page(request):
    return HttpResponse("<h1>This is a success Page.</h1>")
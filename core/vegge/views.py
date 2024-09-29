from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url = '/login/')
def receipes(request):
    if request.method == "POST":
        data = request.POST
        receipe_image = request.FILES.get('receipe_image')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
      
        Receipe.objects.create(
            receipe_image = receipe_image,
            receipe_name = receipe_name,
            receipe_description = receipe_description
        )          
        #print(receipe_description)
        #print(receipe_name)
        #print(receipe_image)
        
        return redirect('/receipes/')

    queryset = Receipe.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))
        
    context = {'receipes' : queryset}
    return render(request , 'receipes.html',context)

def update_receipe(request, id):
    queryset = Receipe.objects.get(id = id)
    
    if request.method == "POST":
        data = request.POST
        receipe_image = request.FILES.get('receipe_image')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')

        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description

        if receipe_image:
            queryset.receipe_image = receipe_image
        
        queryset.save()
        return redirect('/receipes/')
    
    
    context = {'receipe' : queryset}
    return render(request , 'update_receipe.html',context)

def delete_receipe(request, id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete() 
    return redirect('/receipes/')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():  #checking if username exists or not
            messages.info(request, "Username doesn't exist")
            return redirect('/login/')

        user = authenticate(username = username , password = password)
        #checking whether a password corresponding to the username matches or not
        #if it matches an object of user will be returned else None will be returned

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            login(request , user)
            return redirect('/receipes/')
        
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

def register(request):

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username) #this is done to check for existing usernames as its a unique field

        if user.exists():
            messages.info(request, "Username already exists")  #showing a warning in case of an existing username
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)  #this is done to encrypt the password rather storing it as a string
        user.save()

        messages.info(request, "Account created successfully")

        return redirect('/register/')

    return render(request , 'register.html')
from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

def home(request):
	return render(request, 'home.html')

def login(request):
	return render(request, 'login.html') 

@login_required()
def logout(request):
	auth_logout(request)
	return render(request, 'home.html')
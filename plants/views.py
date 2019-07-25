from __future__ import print_function
from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from social_auth.models import UserSocialAuth

def home(request):
  return render(request, 'home.html')

def login(request):
	return render(request, 'login.html') 

@login_required()
def logout(request):
	auth_logout(request)
	return render(request, 'home.html')

@login_required()
def create_event(request):
  creds = UserSocialAuth.get_social_auth_for_user(request.user).get().tokens
    # Save the credentials for the next run
  service = build('calendar', 'v3', credentials=creds)

  event = service.events().insert(calendarId='primary', body=event).execute()
  print('Event created: %s' % (event.get('htmlLink')))

  return render(request, 'home.html')


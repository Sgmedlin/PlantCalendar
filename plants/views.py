from __future__ import print_function
from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
import datetime
import pickle
import os.path
from django.shortcuts import redirect
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from social_django.models import UserSocialAuth
from social_django.utils import load_strategy
from oauth2client.client import AccessTokenCredentials
from .models import Plant
from itertools import cycle
import random


def home(request):
    search_term = ''
    plants_list = Plant.objects.all()
    plant_type = request.GET.get('plant_type', 'All')
    if 'plant_type' in request.GET:
        plant_type = request.GET['plant_type']
    if plant_type != "None" and plant_type != "All" and plant_type != "No":
        plants_list = plants_list.filter(category=plant_type)

    if 'search' in request.GET:
        search_term = request.GET['search']
        plants_list = plants_list.filter(name__icontains=search_term)

    list_of_plants = []
    # if request.user.is_authenticated:
    #     tokens = UserSocialAuth.get_social_auth_for_user(request.user).get().tokens
    #     creds = AccessTokenCredentials(tokens, request.META['HTTP_USER_AGENT'])
    #     service = build('calendar', 'v3', credentials=creds)
    #
    #     calendar_list = service.calendarList().list().execute()
    #
    #     calendar_exists = False
    #     for calendar in calendar_list['items']:
    #         if calendar['summary'] == "Plants":
    #             calendar['backgroundColor'] = "#44a653"
    #             updated_calendar_list_entry = service.calendarList().update(
    #                 calendarId=calendar['id'], body=calendar, colorRgbFormat=True).execute()
    #             calendar_exists = True
    #             created_calendar = calendar
    #
    #     if calendar_exists:
    #         calendar_id = created_calendar["id"]
    #         event_summaries = []
    #         page_token = None
    #         while True:
    #             events = service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
    #             for event in events['items']:
    #                 print(event['summary'])
    #                 event_summaries.append(event['summary'])
    #             page_token = events.get('nextPageToken')
    #             if not page_token:
    #                 break
    #
    #         for summary in event_summaries:
    #             if "start indoors" in summary:
    #                 if "fall" in summary:
    #                     plant_name = summary.strip(" start indoors fall")
    #                 else:
    #                     plant_name = summary.strip(" start indoors")
    #             elif "start outdoors" in summary:
    #                 if "fall" in summary:
    #                     plant_name = summary.strip(" start outdoors fall")
    #                 else:
    #                     plant_name = summary.strip(" start outdoors")
    #             elif "transplant" in summary:
    #                 if "fall" in summary:
    #                     plant_name = summary.strip(" transplant fall")
    #                 else:
    #                     plant_name = summary.strip(" transplant")
    #             else:
    #                 plant_name = summary
    #
    #             print(plant_name)
    #             if plant_name not in list_of_plants:
    #                 list_of_plants.append(plant_name)

    print("---------")
    for plant in list_of_plants:
        print(plant)
    return render(request, 'home.html', {'plants': plants_list, 'plant_type': plant_type, 'list_of_plants': list_of_plants})


def login(request):
    return render(request, 'login.html')


@login_required()
def logout(request):
    auth_logout(request)
    return render(request, 'home.html')


@login_required()
def create_event(request):

    tokens = UserSocialAuth.get_social_auth_for_user(request.user).get().tokens
    creds = AccessTokenCredentials(tokens, request.META['HTTP_USER_AGENT'])
    service = build('calendar', 'v3', credentials=creds)
    calendar_list = service.calendarList().list().execute()

    calendar_exists = False
    for calendar in calendar_list['items']:
        if calendar['summary'] == "Plants":
            calendar['backgroundColor'] = "#44a653"
            updated_calendar_list_entry = service.calendarList().update(
                calendarId=calendar['id'], body=calendar, colorRgbFormat=True).execute()
            calendar_exists = True
            created_calendar = calendar

    if not calendar_exists:
        calendar = {
          "kind": "calendar#calendar",
          "summary": "Plants",
        }
        created_calendar = service.calendars().insert(body=calendar).execute()

    calendar_id = created_calendar["id"]

    selected_plants = request.POST.getlist('checked_plant')

    colors = service.colors().get().execute()

    color_ids_list = []
    for color_id in colors['event']:
        color_ids_list.append(color_id)
        print(color_id)

    random.shuffle(color_ids_list)

    color_pool = cycle(color_ids_list)

    event_summaries = []
    page_token = None
    while True:
        events = service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
        for event in events['items']:
            print(event['summary'])
            event_summaries.append(event['summary'])
        page_token = events.get('nextPageToken')
        if not page_token:
            break

    for plant in selected_plants:
        plant_color = next(color_pool)
        plant_obj = Plant.objects.get(name=plant)
        if plant_obj.start_indoors_begin != "":

            indoors_begin_list = plant_obj.start_indoors_begin.split("-")
            if indoors_begin_list[0] == "Jan":
                start_indoors_begin = "2019-01-" + indoors_begin_list[1]
            elif indoors_begin_list[0] == "Feb":
                start_indoors_begin = "2019-02-" + indoors_begin_list[1]
            elif indoors_begin_list[0] == "Mar":
                start_indoors_begin = "2019-03-" + indoors_begin_list[1]
            elif indoors_begin_list[0] == "Apr":
                start_indoors_begin = "2019-04-" + indoors_begin_list[1]
            elif indoors_begin_list[0] == "May":
                start_indoors_begin = "2019-05-" + indoors_begin_list[1]
            elif indoors_begin_list[0] == "Jun":
                start_indoors_begin = "2019-06-" + indoors_begin_list[1]
            elif indoors_begin_list[0] == "Jul":
                start_indoors_begin = "2019-07-" + indoors_begin_list[1]
            elif indoors_begin_list[0] == "Aug":
                start_indoors_begin = "2019-08-" + indoors_begin_list[1]
            elif indoors_begin_list[0] == "Sep":
                start_indoors_begin = "2019-09-" + indoors_begin_list[1]
            elif indoors_begin_list[0] == "Oct":
                start_indoors_begin = "2019-10-" + indoors_begin_list[1]
            elif indoors_begin_list[0] == "Nov":
                start_indoors_begin = "2019-11-" + indoors_begin_list[1]
            else:
                start_indoors_begin = "2019-12-" + indoors_begin_list[1]

            indoors_end_list = plant_obj.start_indoors_end.split("-")
            if indoors_end_list[0] == "Jan":
                start_indoors_end = "2019-01-" + indoors_end_list[1]
            elif indoors_end_list[0] == "Feb":
                start_indoors_end = "2019-02-" + indoors_end_list[1]
            elif indoors_end_list[0] == "Mar":
                start_indoors_end = "2019-03-" + indoors_end_list[1]
            elif indoors_end_list[0] == "Apr":
                start_indoors_end = "2019-04-" + indoors_end_list[1]
            elif indoors_end_list[0] == "May":
                start_indoors_end = "2019-05-" + indoors_end_list[1]
            elif indoors_end_list[0] == "Jun":
                start_indoors_end = "2019-06-" + indoors_end_list[1]
            elif indoors_end_list[0] == "Jul":
                start_indoors_end = "2019-07-" + indoors_end_list[1]
            elif indoors_end_list[0] == "Aug":
                start_indoors_end = "2019-08-" + indoors_end_list[1]
            elif indoors_end_list[0] == "Sep":
                start_indoors_end = "2019-09-" + indoors_end_list[1]
            elif indoors_end_list[0] == "Oct":
                start_indoors_end = "2019-10-" + indoors_end_list[1]
            elif indoors_end_list[0] == "Nov":
                start_indoors_end = "2019-11-" + indoors_end_list[1]
            else:
                start_indoors_end = "2019-12-" + indoors_end_list[1]

            indoors_event = {
                'colorId': plant_color,
                'summary': plant_obj.name + " start indoors",
                'start': {
                    'date': start_indoors_begin,
                    'timeZone': 'America/New_York',
                },
                'end': {
                    'date': start_indoors_end,
                    'timeZone': 'America/New_York',
                },
                'recurrence': [
                    'RRULE:FREQ=YEARLY'
                ],

            }

            if indoors_event["summary"] not in event_summaries:
                event = service.events().insert(calendarId=calendar_id, body=indoors_event).execute()

        if plant_obj.start_outdoors_begin != "":

            outdoors_begin_list = plant_obj.start_outdoors_begin.split("-")
            if outdoors_begin_list[0] == "Jan":
                start_outdoors_begin = "2019-01-" + outdoors_begin_list[1]
            elif outdoors_begin_list[0] == "Feb":
                start_outdoors_begin = "2019-02-" + outdoors_begin_list[1]
            elif outdoors_begin_list[0] == "Mar":
                start_outdoors_begin = "2019-03-" + outdoors_begin_list[1]
            elif outdoors_begin_list[0] == "Apr":
                start_outdoors_begin = "2019-04-" + outdoors_begin_list[1]
            elif outdoors_begin_list[0] == "May":
                start_outdoors_begin = "2019-05-" + outdoors_begin_list[1]
            elif outdoors_begin_list[0] == "Jun":
                start_outdoors_begin = "2019-06-" + outdoors_begin_list[1]
            elif outdoors_begin_list[0] == "Jul":
                start_outdoors_begin = "2019-07-" + outdoors_begin_list[1]
            elif outdoors_begin_list[0] == "Aug":
                start_outdoors_begin = "2019-08-" + outdoors_begin_list[1]
            elif outdoors_begin_list[0] == "Sep":
                start_outdoors_begin = "2019-09-" + outdoors_begin_list[1]
            elif outdoors_begin_list[0] == "Oct":
                start_outdoors_begin = "2019-10-" + outdoors_begin_list[1]
            elif outdoors_begin_list[0] == "Nov":
                start_outdoors_begin = "2019-11-" + outdoors_begin_list[1]
            else:
                start_outdoors_begin = "2019-12-" + outdoors_begin_list[1]

            outdoors_end_list = plant_obj.start_outdoors_end.split("-")
            if outdoors_end_list[0] == "Jan":
                start_outdoors_end = "2019-01-" + outdoors_end_list[1]
            elif outdoors_end_list[0] == "Feb":
                start_outdoors_end = "2019-02-" + outdoors_end_list[1]
            elif outdoors_end_list[0] == "Mar":
                start_outdoors_end = "2019-03-" + outdoors_end_list[1]
            elif outdoors_end_list[0] == "Apr":
                start_outdoors_end = "2019-04-" + outdoors_end_list[1]
            elif outdoors_end_list[0] == "May":
                start_outdoors_end = "2019-05-" + outdoors_end_list[1]
            elif outdoors_end_list[0] == "Jun":
                start_outdoors_end = "2019-06-" + outdoors_end_list[1]
            elif outdoors_end_list[0] == "Jul":
                start_outdoors_end = "2019-07-" + outdoors_end_list[1]
            elif outdoors_end_list[0] == "Aug":
                start_outdoors_end = "2019-08-" + outdoors_end_list[1]
            elif outdoors_end_list[0] == "Sep":
                start_outdoors_end = "2019-09-" + outdoors_end_list[1]
            elif outdoors_end_list[0] == "Oct":
                start_outdoors_end = "2019-10-" + outdoors_end_list[1]
            elif outdoors_end_list[0] == "Nov":
                start_outdoors_end = "2019-11-" + outdoors_end_list[1]
            else:
                start_outdoors_end = "2019-12-" + outdoors_end_list[1]

            outdoors_event = {
                'colorId': plant_color,
                'summary': plant_obj.name + " start outdoors",
                'start': {
                    'date': start_outdoors_begin,
                    'timeZone': 'America/New_York',
                },
                'end': {
                    'date': start_outdoors_end,
                    'timeZone': 'America/New_York',
                },
                'recurrence': [
                    'RRULE:FREQ=YEARLY'
                ],

            }

            if outdoors_event["summary"] not in event_summaries:
                event = service.events().insert(calendarId=calendar_id, body=outdoors_event).execute()

        if plant_obj.transplant_begin != "":

            transplant_begin_list = plant_obj.transplant_begin.split("-")
            if transplant_begin_list[0] == "Jan":
                transplant_begin = "2019-01-" + transplant_begin_list[1]
            elif transplant_begin_list[0] == "Feb":
                transplant_begin = "2019-02-" + transplant_begin_list[1]
            elif transplant_begin_list[0] == "Mar":
                transplant_begin = "2019-03-" + transplant_begin_list[1]
            elif transplant_begin_list[0] == "Apr":
                transplant_begin = "2019-04-" + transplant_begin_list[1]
            elif transplant_begin_list[0] == "May":
                transplant_begin = "2019-05-" + transplant_begin_list[1]
            elif transplant_begin_list[0] == "Jun":
                transplant_begin = "2019-06-" + transplant_begin_list[1]
            elif transplant_begin_list[0] == "Jul":
                transplant_begin = "2019-07-" + transplant_begin_list[1]
            elif transplant_begin_list[0] == "Aug":
                transplant_begin = "2019-08-" + transplant_begin_list[1]
            elif transplant_begin_list[0] == "Sep":
                transplant_begin = "2019-09-" + transplant_begin_list[1]
            elif transplant_begin_list[0] == "Oct":
                transplant_begin = "2019-10-" + transplant_begin_list[1]
            elif transplant_begin_list[0] == "Nov":
                transplant_begin = "2019-11-" + transplant_begin_list[1]
            else:
                transplant_begin = "2019-12-" + transplant_begin_list[1]

            transplant_end_list = plant_obj.transplant_end.split("-")
            if transplant_end_list[0] == "Jan":
                transplant_end = "2019-01-" + transplant_end_list[1]
            elif transplant_end_list[0] == "Feb":
                transplant_end = "2019-02-" + transplant_end_list[1]
            elif transplant_end_list[0] == "Mar":
                transplant_end = "2019-03-" + transplant_end_list[1]
            elif transplant_end_list[0] == "Apr":
                transplant_end = "2019-04-" + transplant_end_list[1]
            elif transplant_end_list[0] == "May":
                transplant_end = "2019-05-" + transplant_end_list[1]
            elif transplant_end_list[0] == "Jun":
                transplant_end = "2019-06-" + transplant_end_list[1]
            elif transplant_end_list[0] == "Jul":
                transplant_end = "2019-07-" + transplant_end_list[1]
            elif transplant_end_list[0] == "Aug":
                transplant_end = "2019-08-" + transplant_end_list[1]
            elif transplant_end_list[0] == "Sep":
                transplant_end = "2019-09-" + transplant_end_list[1]
            elif transplant_end_list[0] == "Oct":
                transplant_end = "2019-10-" + transplant_end_list[1]
            elif transplant_end_list[0] == "Nov":
                transplant_end = "2019-11-" + transplant_end_list[1]
            else:
                transplant_end = "2019-12-" + transplant_end_list[1]

            transplant_event = {
                'colorId': plant_color,
                'summary': plant_obj.name + " transplant",
                'start': {
                    'date': transplant_begin,
                    'timeZone': 'America/New_York',
                },
                'end': {
                    'date': transplant_end,
                    'timeZone': 'America/New_York',
                },
                'recurrence': [
                    'RRULE:FREQ=YEARLY'
                ],

            }

            if transplant_event["summary"] not in event_summaries:
                event = service.events().insert(calendarId=calendar_id, body=transplant_event).execute()

        if plant_obj.start_indoors_fall_begin != "":

            indoors_fall_begin_list = plant_obj.start_indoors_fall_begin.split("-")
            if indoors_fall_begin_list[0] == "Jan":
                start_indoors_fall_begin = "2019-01-" + indoors_fall_begin_list[1]
            elif indoors_fall_begin_list[0] == "Feb":
                start_indoors_fall_begin = "2019-02-" + indoors_fall_begin_list[1]
            elif indoors_fall_begin_list[0] == "Mar":
                start_indoors_fall_begin = "2019-03-" + indoors_fall_begin_list[1]
            elif indoors_fall_begin_list[0] == "Apr":
                start_indoors_fall_begin = "2019-04-" + indoors_fall_begin_list[1]
            elif indoors_fall_begin_list[0] == "May":
                start_indoors_fall_begin = "2019-05-" + indoors_fall_begin_list[1]
            elif indoors_fall_begin_list[0] == "Jun":
                start_indoors_fall_begin = "2019-06-" + indoors_fall_begin_list[1]
            elif indoors_fall_begin_list[0] == "Jul":
                start_indoors_fall_begin = "2019-07-" + indoors_fall_begin_list[1]
            elif indoors_fall_begin_list[0] == "Aug":
                start_indoors_fall_begin = "2019-08-" + indoors_fall_begin_list[1]
            elif indoors_fall_begin_list[0] == "Sep":
                start_indoors_fall_begin = "2019-09-" + indoors_fall_begin_list[1]
            elif indoors_fall_begin_list[0] == "Oct":
                start_indoors_fall_begin = "2019-10-" + indoors_fall_begin_list[1]
            elif indoors_fall_begin_list[0] == "Nov":
                start_indoors_fall_begin = "2019-11-" + indoors_fall_begin_list[1]
            else:
                start_indoors_fall_begin = "2019-12-" + indoors_fall_begin_list[1]

            indoors_fall_end_list = plant_obj.start_indoors_fall_end.split("-")
            if indoors_fall_end_list[0] == "Jan":
                start_indoors_fall_end = "2019-01-" + indoors_fall_end_list[1]
            elif indoors_fall_end_list[0] == "Feb":
                start_indoors_fall_end = "2019-02-" + indoors_fall_end_list[1]
            elif indoors_fall_end_list[0] == "Mar":
                start_indoors_fall_end = "2019-03-" + indoors_fall_end_list[1]
            elif indoors_fall_end_list[0] == "Apr":
                start_indoors_fall_end = "2019-04-" + indoors_fall_end_list[1]
            elif indoors_fall_end_list[0] == "May":
                start_indoors_fall_end = "2019-05-" + indoors_fall_end_list[1]
            elif indoors_fall_end_list[0] == "Jun":
                start_indoors_fall_end = "2019-06-" + indoors_fall_end_list[1]
            elif indoors_fall_end_list[0] == "Jul":
                start_indoors_fall_end = "2019-07-" + indoors_fall_end_list[1]
            elif indoors_fall_end_list[0] == "Aug":
                start_indoors_fall_end = "2019-08-" + indoors_fall_end_list[1]
            elif indoors_fall_end_list[0] == "Sep":
                start_indoors_fall_end = "2019-09-" + indoors_fall_end_list[1]
            elif indoors_fall_end_list[0] == "Oct":
                start_indoors_fall_end = "2019-10-" + indoors_fall_end_list[1]
            elif indoors_fall_end_list[0] == "Nov":
                start_indoors_fall_end = "2019-11-" + indoors_fall_end_list[1]
            else:
                start_indoors_fall_end = "2019-12-" + indoors_fall_end_list[1]

            indoors_fall_event = {
                'colorId': plant_color,
                'summary': plant_obj.name + " start indoors fall",
                'start': {
                    'date': start_indoors_fall_begin,
                    'timeZone': 'America/New_York',
                },
                'end': {
                    'date': start_indoors_fall_end,
                    'timeZone': 'America/New_York',
                },
                'recurrence': [
                    'RRULE:FREQ=YEARLY'
                ],

            }

            if indoors_fall_event["summary"] not in event_summaries:
                event = service.events().insert(calendarId=calendar_id, body=indoors_fall_event).execute()

        if plant_obj.transplant_fall_begin != "":

            transplant_fall_begin_list = plant_obj.transplant_fall_begin.split("-")
            if transplant_fall_begin_list[0] == "Jan":
                transplant_fall_begin = "2019-01-" + transplant_fall_begin_list[1]
            elif transplant_fall_begin_list[0] == "Feb":
                transplant_fall_begin = "2019-02-" + transplant_fall_begin_list[1]
            elif transplant_fall_begin_list[0] == "Mar":
                transplant_fall_begin = "2019-03-" + transplant_fall_begin_list[1]
            elif transplant_fall_begin_list[0] == "Apr":
                transplant_fall_begin = "2019-04-" + transplant_fall_begin_list[1]
            elif transplant_fall_begin_list[0] == "May":
                transplant_fall_begin = "2019-05-" + transplant_fall_begin_list[1]
            elif transplant_fall_begin_list[0] == "Jun":
                transplant_fall_begin = "2019-06-" + transplant_fall_begin_list[1]
            elif transplant_fall_begin_list[0] == "Jul":
                transplant_fall_begin = "2019-07-" + transplant_fall_begin_list[1]
            elif transplant_fall_begin_list[0] == "Aug":
                transplant_fall_begin = "2019-08-" + transplant_fall_begin_list[1]
            elif transplant_fall_begin_list[0] == "Sep":
                transplant_fall_begin = "2019-09-" + transplant_fall_begin_list[1]
            elif transplant_fall_begin_list[0] == "Oct":
                transplant_fall_begin = "2019-10-" + transplant_fall_begin_list[1]
            elif transplant_fall_begin_list[0] == "Nov":
                transplant_fall_begin = "2019-11-" + transplant_fall_begin_list[1]
            else:
                transplant_fall_begin = "2019-12-" + transplant_fall_begin_list[1]

            transplant_fall_end_list = plant_obj.transplant_fall_end.split("-")
            if transplant_fall_end_list[0] == "Jan":
                transplant_fall_end = "2019-01-" + transplant_fall_end_list[1]
            elif transplant_fall_end_list[0] == "Feb":
                transplant_fall_end = "2019-02-" + transplant_fall_end_list[1]
            elif transplant_fall_end_list[0] == "Mar":
                transplant_fall_end = "2019-03-" + transplant_fall_end_list[1]
            elif transplant_fall_end_list[0] == "Apr":
                transplant_fall_end = "2019-04-" + transplant_fall_end_list[1]
            elif transplant_fall_end_list[0] == "May":
                transplant_fall_end = "2019-05-" + transplant_fall_end_list[1]
            elif transplant_fall_end_list[0] == "Jun":
                transplant_fall_end = "2019-06-" + transplant_fall_end_list[1]
            elif transplant_fall_end_list[0] == "Jul":
                transplant_fall_end = "2019-07-" + transplant_fall_end_list[1]
            elif transplant_fall_end_list[0] == "Aug":
                transplant_fall_end = "2019-08-" + transplant_fall_end_list[1]
            elif transplant_fall_end_list[0] == "Sep":
                transplant_fall_end = "2019-09-" + transplant_fall_end_list[1]
            elif transplant_fall_end_list[0] == "Oct":
                transplant_fall_end = "2019-10-" + transplant_fall_end_list[1]
            elif transplant_fall_end_list[0] == "Nov":
                transplant_fall_end = "2019-11-" + transplant_fall_end_list[1]
            else:
                transplant_fall_end = "2019-12-" + transplant_fall_end_list[1]

            transplant_fall_event = {
                'colorId': plant_color,
                'summary': plant_obj.name + " transplant fall",
                'start': {
                    'date': transplant_fall_begin,
                    'timeZone': 'America/New_York',
                },
                'end': {
                    'date': transplant_fall_end,
                    'timeZone': 'America/New_York',
                },
                'recurrence': [
                    'RRULE:FREQ=YEARLY'
                ],

            }

            if transplant_fall_event["summary"] not in event_summaries:
                event = service.events().insert(calendarId=calendar_id, body=transplant_fall_event).execute()

        if plant_obj.start_outdoors_fall_begin != "":

            outdoors_fall_begin_list = plant_obj.start_outdoors_fall_begin.split("-")
            if outdoors_fall_begin_list[0] == "Jan":
                start_outdoors_fall_begin = "2019-01-" + outdoors_fall_begin_list[1]
            elif outdoors_fall_begin_list[0] == "Feb":
                start_outdoors_fall_begin = "2019-02-" + outdoors_fall_begin_list[1]
            elif outdoors_fall_begin_list[0] == "Mar":
                start_outdoors_fall_begin = "2019-03-" + outdoors_fall_begin_list[1]
            elif outdoors_fall_begin_list[0] == "Apr":
                start_outdoors_fall_begin = "2019-04-" + outdoors_fall_begin_list[1]
            elif outdoors_fall_begin_list[0] == "May":
                start_outdoors_fall_begin = "2019-05-" + outdoors_fall_begin_list[1]
            elif outdoors_fall_begin_list[0] == "Jun":
                start_outdoors_fall_begin = "2019-06-" + outdoors_fall_begin_list[1]
            elif outdoors_fall_begin_list[0] == "Jul":
                start_outdoors_fall_begin = "2019-07-" + outdoors_fall_begin_list[1]
            elif outdoors_fall_begin_list[0] == "Aug":
                start_outdoors_fall_begin = "2019-08-" + outdoors_fall_begin_list[1]
            elif outdoors_fall_begin_list[0] == "Sep":
                start_outdoors_fall_begin = "2019-09-" + outdoors_fall_begin_list[1]
            elif outdoors_fall_begin_list[0] == "Oct":
                start_outdoors_fall_begin = "2019-10-" + outdoors_fall_begin_list[1]
            elif outdoors_fall_begin_list[0] == "Nov":
                start_outdoors_fall_begin = "2019-11-" + outdoors_fall_begin_list[1]
            else:
                start_outdoors_fall_begin = "2019-12-" + outdoors_fall_begin_list[1]

            outdoors_fall_end_list = plant_obj.start_outdoors_fall_end.split("-")
            if outdoors_fall_end_list[0] == "Jan":
                start_outdoors_fall_end = "2019-01-" + outdoors_fall_end_list[1]
            elif outdoors_fall_end_list[0] == "Feb":
                start_outdoors_fall_end = "2019-02-" + outdoors_fall_end_list[1]
            elif outdoors_fall_end_list[0] == "Mar":
                start_outdoors_fall_end = "2019-03-" + outdoors_fall_end_list[1]
            elif outdoors_fall_end_list[0] == "Apr":
                start_outdoors_fall_end = "2019-04-" + outdoors_fall_end_list[1]
            elif outdoors_fall_end_list[0] == "May":
                start_outdoors_fall_end = "2019-05-" + outdoors_fall_end_list[1]
            elif outdoors_fall_end_list[0] == "Jun":
                start_outdoors_fall_end = "2019-06-" + outdoors_fall_end_list[1]
            elif outdoors_fall_end_list[0] == "Jul":
                start_outdoors_fall_end = "2019-07-" + outdoors_fall_end_list[1]
            elif outdoors_fall_end_list[0] == "Aug":
                start_outdoors_fall_end = "2019-08-" + outdoors_fall_end_list[1]
            elif outdoors_fall_end_list[0] == "Sep":
                start_outdoors_fall_end = "2019-09-" + outdoors_fall_end_list[1]
            elif outdoors_fall_end_list[0] == "Oct":
                start_outdoors_fall_end = "2019-10-" + outdoors_fall_end_list[1]
            elif outdoors_fall_end_list[0] == "Nov":
                start_outdoors_fall_end = "2019-11-" + outdoors_fall_end_list[1]
            else:
                start_outdoors_fall_end = "2019-12-" + outdoors_fall_end_list[1]

            outdoors_fall_event = {
                'colorId': plant_color,
                'summary': plant_obj.name + " start outdoors fall",
                'start': {
                    'date': start_outdoors_fall_begin,
                    'timeZone': 'America/New_York',
                },
                'end': {
                    'date': start_outdoors_fall_end,
                    'timeZone': 'America/New_York',
                },
                'recurrence': [
                    'RRULE:FREQ=YEARLY'
                ],

            }

            if outdoors_fall_event["summary"] not in event_summaries:
                event = service.events().insert(calendarId=calendar_id, body=outdoors_fall_event).execute()

    return redirect(home)


import os
import json
import requests

from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

from .models import Greeting
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

@csrf_exempt
def createToken(request):

    content = request.GET
    # get the identity from the request, or make one up
    identity = request.user.username
    # get credentials for environment variables
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    api_key = os.environ['TWILIO_API_KEY']
    api_secret = os.environ['TWILIO_API_SECRET']
    chat_service_sid = os.environ.get('TWILIO_CHAT_SERVICE_SID', None)

    # Create access token with credentials
    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create an Chat grant and add to token
    if chat_service_sid:
        chat_grant = ChatGrant(service_sid=chat_service_sid)
        token.add_grant(chat_grant)
        
    # Return token info as JSON
    return JsonResponse(data={"identity": identity, "token": token.to_jwt().decode('utf-8')}, safe=False)

def chat(request):

    return render(request, 'chat.html', {})

def user_logged_in(request):

    account = os.environ['TWILIO_ACCOUNT_SID']
    token = os.environ['TWILIO_AUTH_TOKEN']
    chat_service_sid = os.environ.get('TWILIO_CHAT_SERVICE_SID', None)
    client = Client(account, token)

    try:
        channel = client.chat.services(chat_service_sid).channels(request.user.username + "_chat_channel").fetch()
    except:
        channel = client.chat.services(chat_service_sid).channels.create(unique_name=request.user.username + "_chat_channel", friendly_name=request.user.username)

    return JsonResponse(data={"username": request.user.username, "channel": channel.unique_name, "user_id": request.user.id, "first_name": request.user.first_name, "last_name": request.user.last_name}, safe=False)

def user_chat_join(request):
    user_data = request.GET
    user_selected = User.objects.get(pk=user_data["id"])
    account = os.environ['TWILIO_ACCOUNT_SID']
    token = os.environ['TWILIO_AUTH_TOKEN']
    chat_service_sid = os.environ.get('TWILIO_CHAT_SERVICE_SID', None)
    client = Client(account, token)

    try:
        channel = client.chat.services(chat_service_sid).channels(user_selected.username + "_chat_channel").fetch()
    except:
        channel = client.chat.services(chat_service_sid).channels.create(unique_name=user_selected.username+ "_chat_channel", friendly_name=user_selected.username)

    return JsonResponse(data={"username": user_selected.username, "channel": channel.unique_name, "user_id": user_selected.id, "first_name": user_selected.first_name, "last_name": user_selected.last_name}, safe=False)

def user_chat_start(request):

    return render(request, 'chat_join.html', {})
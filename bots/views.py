from django.shortcuts import render
from bots.models import *


# Create your views here.

def index(request):
    return render(request, 'bots/test.html', {})

def show_profile(request, profile_name):
    # try to retrieve info about player
    try:
        player = Player.objects.get(user__username = profile_name)
        context = {'player': player}
    except: # player not found
        context = {'player': None}
    
    return render(request, 'bots/profile.html', context)
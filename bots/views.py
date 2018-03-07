from django.shortcuts import render
from bots.models import *
# Create your views here.

def index(request):
    return render(request, 'bots/test.html', {})

def show_profile(request, profile_name):
    # try to retrieve info about player
    try:
        player = Player.objects.get(user__username = profile_name)
        number_of_robots = len(Robot.objects.filter(owner = player))
        followees = player.follows.all()
        top5_valuable__robots = Robot.objects.filter(owner=player).order_by('-value')[:5]
        top5_winning__robots = Robot.objects.filter(owner=player).order_by('-wins')[:5]
        context = {
            'player': player,
            # number of robots the player owns
            'number_of_robots' : number_of_robots,
            # players this player is following 
            'followees' : followees,
            # the 5 most valuable robots the player owns
            'top5_valuable_robots' : top5_valuable_robots,
            # top5 robots with the most wins
            'top5_winning_robots' : top5_winning__robots,
        }
            
    except: # player not found
        context = {'player': None}
    
    return render(request, 'bots/profile.html', context)
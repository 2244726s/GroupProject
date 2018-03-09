from django.shortcuts import render
from bots.models import *
from bots.forms import *
# Create your views here.

def index(request):
    context =  {'bot' : Robot.objects.all()[0]}
    return render(request, 'bots/index.html', context)

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

def upgrade(request):
    ''' ajax view used for increasing stats of robots'''
    if request.method == 'GET':
        stat = request.GET['stat']
        bot_id = int(request.GET['bot_id'])
    
        #try to  find robot with given id
        try:
            bot = Robot.objects.get(id=bot_id)
        except: # invalid robot id
            print('upgrade was called with invalid robot id!!!')    
            # assume player has enough scrap, since otherwise they wouldnt have access to button that calls this
        
        if(stat == 'speed'):
            bot.owner.scrap -= bot.speed*25
            bot.speed += 1
        elif(stat == 'dodge'):
            bot.owner.scrap -= bot.dodge*25
            bot.dodge+= 1
        elif(stat == 'armour'):
            bot.owner.scrap -= bot.armour*25
            bot.armour+= 1
        elif(stat == 'weapon'):
            bot.owner.scrap -= bot.weapon*25
            bot.weapon+= 1
        elif(stat == 'accuracy'):
            bot.owner.scrap -= bot.accuracy*25
            bot.accuracy+= 1

        bot.save() 
        bot.owner.save()
        # returned new rendered table
        response =  render(request, 'bots/bot_table.html', {
            'robot' : bot,
            'stats' : bot.get_stats(),
            'player' : bot.owner,})
        return response

def leaderboards(request):
    return render(request, 'bots/leaderboards.html')

def about(request):
    return render(request, 'bots/about.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'bots/signin.html', {})
    return render(request, 'bots/signin.html')


def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'bots/signup.html',{'user_form': user_form,'registered': registered})


    




from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from bots.models import *
from bots.forms import *
from bots.matchmaking import matchmake, get_matches
# Create your views here.

def index(request):
    context =  {'bot' : Robot.objects.all()[0]}
    return render(request, 'bots/index.html', context)

def show_profile(request, profile_name):
    # try to retrieve info about player
    try:
        player = Player.objects.get(user__username = profile_name)
    except: # no player found
        context = {'player': None}

    if player:
        context = {
            'player': player,
            # number of robots the player owns
            'number_of_robots' : len(Robot.objects.filter(owner = player)),
            # players this player is following
            'followees' : player.follows.all(),
            # the 5 most valuable robots the player owns
            'top5_valuable_robots' : Robot.objects.filter(owner=player).order_by('-value')[:5],
            # top5 robots with the most wins
            'top5_winning_robots' : Robot.objects.filter(owner=player).order_by('-wins')[:5],
            # list of player's robots
            'robots' : Robot.objects.filter(owner=player),
            # list of stat names
            'stats' : ['speed', 'dodge', 'armour', 'weapon', 'accuracy'],
        }

    return render(request, 'bots/profile.html', context)

def upgrade(request):
    ''' ajax view used for increasing stats of robots'''
    if request.method == 'GET':
        stat = request.GET.get('stat',"")
        bot_name = request.GET.get('bot_name',"")

        #try to  find robot with given id
        try:
            bot = Robot.objects.get(name = bot_name)

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
        except: # invalid robot id
            print('upgrade was called with invalid robot id!!!')
            # assume player has enough scrap, since otherwise they wouldnt have access to button that calls this
            return render(request, 'bots/bot_table.html',{'message': bot_name})



def display_bot(request):
    print("Test2")
    if request.method == "GET":
        bot_name = request.GET.get('bot_name','')


        try:
            bot = Robot.objects.get(name = bot_name)
            response =  render(request, 'bots/bot_table.html', {
            'robot' : bot,
            'stats' : bot.get_stats(),
            'player' : bot.owner,})
            return response
        except:
            return render(request,'bots/bot_table.html',{})

def validate(request):
    if request.method == "GET":
        size = int(request.GET.get('size',0))
        name = request.GET.get('name','')
        returner = {}
        bots = []
        valid = True
        bot_names = []

        msg = 'everything works'
        player = Player.objects.get(user__username = name)
        for i in range(size):
            bot_names.append(request.GET.get('b' + str(i),''))


        for i in range(size):
            for j in range(i + 1,size):

                if bot_names[i] == bot_names[j]:
                    valid = False
                    msg = 'duplicate bot found'

        try:
            bots.append(Robot.objects.get(name = bot_names[i]))
        except:
            valid = False
            'bot ' + bot_names[i] + ' not found'


        valid = valid and len(bots) > 0
        if valid:

            try:
                t = Team.objects.get(player = player, num_bots = len(bots))
            except:
                t = None

            duplicate = True
            if t:

                for i in t.bots.all():
                    for j in bots:
                        if i.name != j.name:
                            duplicate = False

                if duplicate:
                    games = get_matches(t)
                    msg = 'team found'
                else:
                    games = matchmake(player, bots)
                    msg = 'team made'

            else:
                games = matchmake(player, bots)
                msg = 'team made'

            return render(request,'bots/matchmake.html',{
                'valid':True,
                'robots':bots,
                'player':name,
                'games':games,
                'team':bot_names,
                'size':size,
                'msg':msg,
            })



        else:
            bots = Robot.objects.filter(owner = player)
            return render(request,'bots/matchmake.html',{
                'valid':False,
                'robots':bots,
                'player':name,
                'team':bot_names,
                'size':size,
                'msg':msg,
                })

def resetTeam(request):
    if request.method == 'GET':
        size = int(request.GET.get('size',0))
        name = request.GET.get('name','')

        player = Player.objects.get(user__username = name)
        bot_names = []
        bots = Robot.objects.filter(owner = player)
        for i in range(size):
            bot_names.append(request.GET.get('b' + str(i),''))

        return render(request, 'bots/matchmake.html',{'valid':False, 'team':bot_names,'robots':bots,'games':'','size':size, 'msg':'please update your team:'})

def initialize(request):
    if request.method == 'GET':
        size = int(request.GET.get('size',0))
        name = request.GET.get('name','')

        player = Player.objects.get(user__username = name)
        if player:

            try:
                t = Team.objects.get(player = player, num_bots = size)
            except:
                t = None

            if t:
                matches = get_matches(t)
                return render(request, 'bots/matchmake.html',{'valid':True, 'team':[i.name for i in t.bots.all()],'games':matches,'size':size, 'msg':'Team found everything worked'})

            else:
                bots = Robot.objects.filter(owner = player)
                return render(request, 'bots/matchmake.html',{'valid':False,'robots':bots,'size':size,'team':range(size),'msg':'no team found'})

        else:
            return render(request, 'bots/matchmake.html',{'valid':False, 'size':size,'msg':'player not found: ' + name})




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
                return HttpResponse("Your account is disabled.")
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




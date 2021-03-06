


from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from bots.models import *
from bots.forms import *
from bots.matchmaking import matchmake, get_matches, challenge
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    context =  {'players' : Player.objects.all().order_by('-user__date_joined')[:5]}
    # shows the 5 most newest players
    return render(request, 'bots/index.html', context)


def show_profile(request, profile_name):
    # try to retrieve info about player
    try:
        player = Player.objects.get(user__username = profile_name)
    except: # no player found
        player = None
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
            'battleHistory' : Battle.objects.filter(participants = player).order_by('-date')
        }
        #returns information about a player so that their profile can be rendered

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
                'player' : bot.owner,
                'editable': True})
            return response
        except: # invalid robot id
            print('upgrade was called with invalid robot id!!!')
            # assume player has enough scrap, since otherwise they wouldnt have access to button that calls this
            return render(request, 'bots/bot_table.html',{'message': bot_name})



def display_bot(request):
    if request.method == "GET":
        bot_name = request.GET.get('bot_name','')
        # retrieves information about a robot so that it can be displayed

        try:
            bot = Robot.objects.get(name = bot_name)
            if bot.owner.user.username == request.user.username:
                editable = True
            else:
                editable = False
                # boolean flag to indicate if the user will be able to upgrade this robot

            response =  render(request, 'bots/bot_table.html', {
            'robot' : bot,
            'stats' : bot.get_stats(),
            'player' : bot.owner,
            'editable':editable,})
            return response
        except:
            return render(request,'bots/bot_table.html',{})





def validate(request):
    # validates a list of robots to check if they are unique and accessible,
    # if valid it will then begin the matchmaking process and render lists of which can be played
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
            # generates 2 lists of games (ones who have challened me, and ones who I am able to challenge) and the newly formed team
            received, sent, t = matchmake(player, bots, size)

            return render(request, 'bots/matchmake.html',{'valid':True, 'team':[i.name for i in t.bots.all()],'received':received,'sent':sent, 'size':size, 'msg':'Team found everything worked'})


        else:
            # the team was invalid so the matchmaking doesn't happen
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
    #removes a players current team so that it can be updated
    if request.method == 'GET':
        size = int(request.GET.get('size',0))
        name = request.GET.get('name','')
        team = Team.objects.get(player = name, num_bots = size)
        team.delete()
        #deletes old team

        player = Player.objects.get(user__username = name)
        bot_names = []
        bots = Robot.objects.filter(owner = player)
        for i in range(size):
            bot_names.append(request.GET.get('b' + str(i),''))
        # git list of all robots owned by the player so that they are eligable to be added to the team

        return render(request, 'bots/matchmake.html',{'valid':False, 'team':bot_names,'robots':bots,'games':'','size':size, 'msg':'please update your team:'})


def initialize(request):
    # used to retrieve matchmaking info when a page is first loaded
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
                received, sent = get_matches(t, size)
                try:
                    # checks if player has already challenged a different player
                    challenge = Challenge.objects.get(challenger = t, num_bots = size)
                    return render(request, 'bots/matchmake.html',{'valid':True, 'team':[i.name for i in t.bots.all()],'received':received,'sent':sent,'challengee':challenge.challengee, 'size':size, 'msg':'Team found everything worked'})
                except:
                    # else displays list of possible matches
                    return render(request, 'bots/matchmake.html',{'valid':True, 'team':[i.name for i in t.bots.all()],'received':received,'sent':sent, 'size':size, 'msg':'Team found everything worked'})

            else:
                # no current team, so player must make one in order to matchmake
                bots = Robot.objects.filter(owner = player)
                return render(request, 'bots/matchmake.html',{'valid':False,'robots':bots,'size':size,'team':range(size),'msg':'no team found'})

        else:
            # error no player found so returns a message saying that no player was found
            return render(request, 'bots/matchmake.html',{'valid':False, 'size':size,'msg':'player not found: ' + name})


def fight(request):
    # sends a battle request to another player
    if request.method == 'GET':
        name = request.GET.get('name','')
        size = int(request.GET.get('size',''))
        opponent = request.GET.get('opponent','')


        me = Player.objects.get(user__username = name)
        them = Player.objects.get(user__username = opponent)


        my_team = Team.objects.get(player = me, num_bots = size)
        dbug = challenge(me, them,size, my_team.bots.all())

        if(dbug == 0):
            # you have accepted another players challenge and the battle has been completed
            return HttpResponse('Accepted challenge from '+ opponent)
        elif(dbug == 1):
            # you have sent a challenge to another player but they have not yet accepted it
            return HttpResponse('Challenge Sent to '+ opponent + ' they must accept before the match commences')
        else:
            # you have already sent a different player a challenge and cannot send one to another
            return HttpResponse('You Have already challenged ' + opponent +', you may not challenge another player yet')








def validate_name(request):
    # checks to see if the name given to a new robot is
    if request.method == 'GET':
        name = request.GET.get('name','')
        type = request.GET.get('type','')
        if Robot.objects.filter(name = name).count() == 0:
            return HttpResponse(name + ' is available')
        return HttpResponse(name + ' is already in use')


@csrf_exempt
def create_bot(request):
    # validates to check if a name is unique, then creates the attributes of the robot based off its type
    if request.method == 'GET':
        name = request.GET.get('name','error')
        type = request.GET.get('type','error')
        try:
            player = Player.objects.get(user = request.user)
        except:
            player = None

        if player:

            try:
                bot = Robot.objects.get(name = name)
                if bot:
                    return HttpResponse('name error-'+ name + str(Robot.objects.filter(name = name).count()))
            except:
                #name isn't taken
                player.scrap -= 10
                player.save()

                if type == 'aerial':
                    r = Robot.objects.create(name = name, owner = player, value = 7)
                    r.type = type
                    r.speed = 2
                    r.dodge = 4
                    r.armour = 1
                    r.weapon = 2
                    r.accuracy = 2
                    r.save()

                elif type == 'bipedal':
                    r = Robot.objects.create(name = name, owner = player, value = 7)
                    r.type = type
                    r.speed = 4
                    r.dodge = 2
                    r.armour = 2
                    r.weapon = 2
                    r.accuracy = 1
                    r.save()

                elif type == 'wheeled':
                    r = Robot.objects.create(name = name, owner = player, value = 7)
                    r.type = type
                    r.speed = 1
                    r.dodge = 2
                    r.armour = 4
                    r.weapon = 2
                    r.accuracy = 2
                    r.save()

                else:
                    return HttpResponse('type error-' + type)

                return HttpResponseRedirect('')
                # returns to page
        else:
            return HttpResponse('player error')
    else:
        return HttpResponse(request.method)

def leaderboards(request):
    # gets data about the most winning robots, and the most winning players
    context = {
        'top_bots' : Robot.objects.order_by('-wins')[:10],
        'top_users' : Player.objects.order_by('-wins')[:10]
        }

    return render(request, 'bots/leaderboards.html', context)

def about(request):
    # renders the about page
    return render(request, 'bots/about.html')

def signin(request):
    # validates a users attempt to sign in
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
    return render(request, 'bots/signin.html',{})


def signup(request):
    # processes a new users attempt to sign up
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            Player.objects.create(user = user, scrap = 10)
            login(request, user)
            return render(request, 'bots/index.html',{'players' : Player.objects.all().order_by('-user__date_joined')[:5]})
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'bots/signup.html',{'user_form': user_form,'registered': registered})

@login_required
def signout(request):
    # allows a user to sign out, only rendered to users who are currently signed in
    logout(request)
    return HttpResponseRedirect(reverse('index'))


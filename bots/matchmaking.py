"""
methods for finding matches for players
"""
from bots.models import Player, Robot, Challenge, Team
from bots.mechanics import battle
import json

def challenge(player1, player2,size, sorted_robots):
    # check if the challengee already issued a challenge to the challenger
    try:
        challenger_team = Team.objects.get(player = player1, num_bots = size)
        challengee_team = Team.objects.get(player = player2, num_bots = size)
    except:
        print("something has gone wrong, I think the tests need to be updated")


    try:
        challenge = Challenge.objects.get(challenger=challengee_team, challengee=challenger_team, num_bots = len(sorted_robots))
    except:
        challenge = None
    if(challenge):
        # get info from the challenge about the other player's robots
        # battle
        battle(sorted_robots, challengee_team.bots.all())
        # delete challenge from DB
        challenge.delete()
    else: # counter challenge doesnt yet exist
        # create challenge
        challenger_team.robots = sorted_robots
        challenger_team.save()
        c = Challenge(challenger = challenger_team, challengee=challengee_team, num_bots = len(sorted_robots))
        c.save()
        # add all the robots


def matchmake(player, robots, size, i = 10):
    teams = Team.objects.filter(player = player, num_bots = size)
    if teams:
        teams.delete()

    t = Team.objects.create(player = player, num_bots = size)
    t.save()
    for robot in robots:
        t.bots.add(robot)
    t.save()
    # update players robot roster before searching for new matches

    challenges = find_challenge(t,size, i)
    remainder = i - len(challenges)
    if remainder > 0:
        challenges += create_challenge(t,size, remainder)
    return challenges


def get_matches(t,size ,i = 10):

    challenges = find_challenge(t, size,i)
    remainder = i - len(challenges)
    if remainder > 0:
        challenges += create_challenge(t, size, remainder)
    return challenges

def sorti(best_fit, i):

    returner = []
    #iterator
    listify = list(best_fit.keys())
    while(len(returner) < len(best_fit.keys()) and len(returner) <= i):

        min = listify[0]

        for key in listify:
            if (best_fit[min] > best_fit[key]) and key not in returner:
                min = key
        listify.remove(min)
        returner.append(min)

    return returner


def find_challenge(my_team,size, i):
    # finds the best i challenges that I have received

    seekers = Challenge.objects.filter(num_bots = size).filter(challengee = my_team)
    #find all teams of the same size as mine who have challenged me
    # __ is used to access properties of the foreign key

    best_fit = {}
    my_scrap = sum([i.value for i in my_team.bots.all()])
    for seeker in seekers:
        their_scrap = sum([i.value for i in seeker.challenger.bots.all()])
        best_fit[seeker.challenger] = abs(their_scrap - my_scrap)
        # get heuristic for best match

    matches = sorti(best_fit,i)

    return matches




def create_challenge(my_team,size, i):

    seekers = Team.objects.exclude(player = my_team.player).filter(num_bots = size)
    my_scrap = sum([i.value for i in my_team.bots.all()])

    best_fit = {}

    for seeker in seekers:
        their_scrap = sum([i.value for i in seeker.bots.all()])
        best_fit[seeker] = abs(their_scrap - my_scrap)

    return sorti(best_fit,i)



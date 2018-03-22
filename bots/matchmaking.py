"""
methods for finding matches for players
"""
from bots.models import Player, Robot, Challenge, Team
from bots.mechanics import battle
import json

def challenge(player1, player2, sorted_robots):
    # check if the challengee already issued a challenge to the challenger
    try:
        challenger_team = Team.objects.get(player = player1, num_bots = len(sorted_robots))
        challengee_team = Team.objects.get(player = player2, num_bots = len(sorted_robots))
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


def find_match(player):
	# list of players looking for match
	seekers = Player.objects.filter(looking_for_match = True)
	# check if there are at least 10 players looking for match
	if(len(seekers>= 10)):
		# find opponent with closest value of robots
		opponent = seekers[0]
		for seeker in seekers:
			# check if seeker's robot scrap value is closer to to player's robot's scrap value
			if abs(player.chosen_robot.value - seeker.chosen_robot.value) < abs(player.chosen_robot.value - opponent.chosen_robot.value):
				opponent = seeker

		# battle(player.chosen_robot, opponent.chosen__robot)
		# unflag opponent from looking for match
		opponent.looking_for_match = False
		opponent.save()

	else: # list of players looking for match is less than ten
		# flag the player as llooking for match
		player.looking_for_match = True
		player.save()


def matchmake(player, robots, i = 10):
    teams = Team.objects.filter(player = player, num_bots = len(robots))
    if teams:
        teams.delete()

    t = Team.objects.create(player = player, num_bots = len(robots))
    t.save()
    for robot in robots:
        t.bots.add(robot)
    t.save()
    # update players robot roster before searching for new matches

    challenges = find_challenge(t, i)
    remainder = i - len(challenges)
    if remainder > 0:
        challenges += create_challenge(t, remainder)
    return challenges


def get_matches(t,i = 10):

    challenges = find_challenge(t,i)
    remainder = i - len(challenges)
    if remainder > 0:
        challenges += create_challenge(t, remainder)
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


def find_challenge(my_team, i):
    # finds the best i challenges that I have received

    seekers = Challenge.objects.filter(num_bots = my_team.num_bots).filter(challengee = my_team)
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




def create_challenge(my_team, i):

    seekers = Team.objects.exclude(player = my_team.player).filter(num_bots = my_team.num_bots)
    my_scrap = sum([i.value for i in my_team.bots.all()])

    best_fit = {}

    for seeker in seekers:
        their_scrap = sum([i.value for i in seeker.bots.all()])
        best_fit[seeker] = abs(their_scrap - my_scrap)

    return sorti(best_fit,i)



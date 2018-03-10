"""
methods for finding matches for players
"""
from bots.models import Player, Robot, Challenge, Team
from bots.mechanics import battle
import json

def challenge(challenger, challengee, sorted_robots):
    # check if the challengee already issued a challenge to the challenger
    challenger_team = Team.objects.get(player = challenger, num_bots = len(sorted_robots))
    challengee_team = Team.objects.get(player = challengee, num_bots = len(sorted_bots))
    try:
        challenge = Challenge.objects.get(challenger=challengee_team, challengee=challenger_team)
    except:
        challenge = None
    if(challenge):
        # get info from the challenge about the other player's robots
        # battle
        battle(sorted_robots, challengee_team.robots)
        # delete challenge from DB
        challenge.delete()
    else: # counter challenge doesnt yet exist
        # create challenge
        challenger_team.robots = sorted_robots
        challenger_team.save()
        c = Challenge(challenger = challenger, challengee=challengee)
        c.save()
        # add all the robots
        for r in robots:
            c.robots.add(r)
        # save again to commit all changes
        c.save()

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
    teams = Team.objects.filter(player = player)
    teams.delete()
    t = Team(player = player, robots = robots, num_bots = len(robots))
    teams.save()
    # update players robot roster before searching for new matches

    challenges = find_challenge(player, robots, i)
    remainder = i - len(challenges)
    if i > 0:
        challenges += create_challenge(player, robots, remainder)
    return json.dumps(challenges)

def sorti(best_fit, i):

    returner = []
    #iterator

    while(len(returner) < len(best_fit.keys()) and len(returner) < i):
        min = best_fit.keys()[0]

        for key in best_fit.keys():
            if (best_fit[min] > best_fit[key]) and key not in returner:
                min = key

        returner.add(min)

    return returner


def find_challenge(player, robots, i):
    # finds the best i challenges that I have received
    seekers = Challenge.objects.filter(num_bots = len(robots)).filter(challengee = player)
    #find all teams of the same size as mine who have challenged me

    best_fit = {}
    my_scrap = sum([i.value for i in robots])
    for seeker in seekers:
        their_scrap = sum([i.value for i in seeker.challenger.bots])
        best_fit[seeker] = abs(their_scrap - my_scrap)
        # get heuristic for best match

    matches = sorti(best_fit,i)

    return matches




def create_challenge(player, robots, i):

    seekers = Teams.objects.exclude(player = player).filter(num_bots = len(robots))
    my_scrap = sum([i.value for i in robots])

    best_fit = {}

    for seeker in seekers:
        their_scrap = sum([i.value for i in seeker.robots])
        best_fit[seeker] = abs(their_scrap - my_scrap)

    return sorti(best_fit,i)




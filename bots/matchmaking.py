"""
methods for finding matches for players
"""
from bots.models import Player, Robot, Challenge 
from bots.mechanics import battle

def challenge(challenger, challengee, robots):
    # check if the challengee already issued a challenge to the challenger
    try:
        challenge = Challenge.objects.get(challenger=challengee, challengee=challenger)
    except:
        challenge = None
    if(challenge):
        # get info from the challenge about the other player's robots
        robots2 = challenge.robots.all()
        # battle
        battle(robots, robots2)
    else: # counter challenge doesnt yet exist
        # create challenge
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
		
	
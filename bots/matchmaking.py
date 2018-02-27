"""
methods for finding matches for players
"""
from models import Player, Robot

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
		
	
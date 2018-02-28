"""
contains various functions for game mechanics related computations 
"""
from models import Player, Robot, Battle

# constants for robot types to be used so that database doesn't get corrupted accidently
AERIAL = 'aerial'
BIPEDAL = 'bipedal'
WHEELED = 'wheeled'

def battle(robot1, robot2):
    """
    Takes two robots, simulates a battle, and makes adjustments to database accordinngly.
    """
    
    # for storing the battle log with details of turn by turn action, which user will view when reviewing this battle
    log = ""
    
    # insert battle simulation code here 
    
    # at the end of the battle, winning robot and losing robot should be determined and stored in variables : 'losing_robot' and 'winning_robot'
    
    # update player robot statistics 
    winner = winning_robot.owner
    loser = losing_robot.owner
    
    winner .wins += 1
    loser.losses += 1
    
    losing_robot.losses+= 1
    winning_robot.wins += 1
    
    
    # awardscrap reward to winner
    # REPLACE WITH ACTUAL AMOUNT AS DETERMINED BY MECHANICS
    winner.scrap += 0
    
    # create Battle object storing info about the battle
    b = Battle(log = log)
    b.participants.add(winner)
    b.participants.add(loser)
    b.save()
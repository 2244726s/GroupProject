"""
contains various functions for game mechanics related computations
"""

from bots.models import Player, Robot, Battle
import math
import random
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

    delay1 = -1 * robot1.speed
    delay2 = -1 * robot2.speed
    # determines who attacks first
    health1 = 8 + (math.ceil(float(robot1.armour) / 2.0))
    health2 = 8 + (math.ceil(float(robot2.armour) / 2.0))

    while(health1 > 0 or health2 > 0):
        if(delay1 < delay2):
            damage = attack(robot1,robot2)
            health2 -= damage
            delay1 += robot1.speed
            log = log + updateLog(robot1,robot2,damage)
        else:
            damage = attack(robot2,robot1)
            health1 -= damage
            delay2 += robot2.speed
            log = log + updateLog(robot1,robot2,damage)

        log = log + "\n new round"

    if(health1 > 0):
        # robot1 won
        winning_robot = robot1
        losing_robot = robot2

    else:
        # robot2 won
        winning_robot = robot2
        losing_robot = robot1


    log = log + "\n %s has been Destroyed! %s is Victorious!" % (losing_robot,winning_robot)


    # update player robot statistics
    winner = winning_robot.owner
    loser = losing_robot.owner

    winner .wins += 1
    loser.losses += 1

    losing_robot.losses+= 1
    winning_robot.wins += 1


    # awardscrap reward to winner
    # REPLACE WITH ACTUAL AMOUNT AS DETERMINED BY MECHANICS
    winner.scrap += 40
    loser.scrap += 10

    # create Battle object storing info about the battle
    b = Battle(log = log)
    b.save()
    b.participants.add(winner)
    b.participants.add(loser)
    b.save()


def updateLog(attacker, defender, damage):
    if(damage > 0):
        return "\n %s attacked %s for %d damage" % (attacker.name, defender.name, damage)
    else:
        return "\n %s dodged %s's attack" % (defender.name, attacker.name)




def attack(attacker,defender):
    #returns integer showing how much damage the attack did

    accuracy = attacker.accuracy
    if(attacker.type == WHEELED and defender.type == BIPEDAL):
        accuracy+=1

    dodge = defender.dodge
    if(attacker.type == BIPEDAL and defender.type == AERIAL):
        dodge+=1

    hitChance = float(accuracy)/float(accuracy+dodge)
    if(hitChance > random.uniform(0,1)):
        if(attacker.type == AERIAL and defender.type == WHEELED):
            return attacker.weapon + 1
        else:
            return attacker.weapon
    else:
        return 0
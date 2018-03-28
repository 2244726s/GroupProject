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

def battle(robots1, robots2):
    """
    Takes two robots, simulates a battle, and makes adjustments to database accordinngly.
    """
    log = ""
    robot1 = robots1[0]
    robot2 = robots2[0]

    index1 = 0
    index2 = 0


    health1 = 8 + (math.ceil(float(robot1.armour) / 2.0))
    health2 = 0

    # log
    # for storing the battle log with details of turn by turn action, which user will view when reviewing this battle


    p1win = True
    winHealth = 8 + (math.ceil(float(robot2.armour) / 2.0))
    # ensures that the newest robot comes in at full health, rather than the health of their predecessor i.e. 0

    while(index1 < len(robots1) and index2 < len(robots2)):
        robot1 = robots1[index1]
        robot2 = robots2[index2]

        if(p1win):
            #robot1 won the previous match and therefore keeps the same health
            health1 = winHealth
            health2 = 8 + (math.ceil(float(robot2.armour) / 2.0))

        else:
            #robot2 won the previous match and therefore keeps the same health
            health2 = winHealth
            health1 = 8 + (math.ceil(float(robot1.armour) / 2.0))

        delay1 = -1 * robot1.speed
        delay2 = -1 * robot2.speed
    # determines who attacks first

        while(health1 > 0 and health2 > 0):
            if(delay1 < delay2):
                damage = attack(robot1,robot2)
                health2 -= damage
                delay1 += robot1.speed
                log = log + updateLog(robot1,robot2,damage, health2)
            else:
                damage = attack(robot2,robot1)
                health1 -= damage
                delay2 += robot2.speed
                log = log + updateLog(robot2,robot1,damage, health1)
    # simulates battle between 2 robots



        if(health1 > 0):
            # robot1 won
            p1win = True
            winHealth = health1
            log = log + "\n %s has been destroyed!"%(robot2.name)
            index2 += 1
            if(index2 < len(robots2)):
                log = log + ", %s has entered the frey!"%(robots2[index2].name)

        else:
            # robot2 won
            p1win = False
            winHealth = health2
            log = log + "\n \n %s has been destroyed!"%(robot1.name)
            index1 += 1
            if(index1 < len(robots1)):
                log = log + ", %s has entered the frey! \n"%(robots1[index1].name)
        #updates log and robot roster

    winner_scrap = 0
    loser_scrap = 0
    if(index1 >= len(robots1)):
        #player2 won
        winner_scrap = math.fsum([i.value for i in robots2])
        loser_scrap = math.fsum([i.value for i in robots1])
        winner = robots2[0].owner
        loser = robots1[0].owner

        for bot in robots2:
            bot.wins += 1
            bot.save()

        for bot in robots1:
            bot.losses += 1
            bot.save()

    else:
        # player1 won
        winner = robots1[0].owner
        loser = robots2[0].owner

        winner_scrap = math.fsum([i.value for i in robots1])
        loser_scrap = math.fsum([ i.value for i in robots2])

        for bot in robots1:
            bot.wins += 1
            bot.save()
        for bot in robots2:
            bot.losses += 1
            bot.save()

    reward_scrap = get_scrap(len(robots1),winner_scrap,loser_scrap)
    log = log + "\n %s won!"%(str(winner))
    # debugging purposes only: log = log + "\n \n %s gets %d scrap and %s gets %d scrap"%(str(winner),reward_scrap,str(loser),reward_scrap/5)
    winner.wins += 1
    loser.losses += 1




    # awardscrap reward to winner
    # REPLACE WITH ACTUAL AMOUNT AS DETERMINED BY MECHANICS
    winner.scrap += reward_scrap
    loser.scrap += reward_scrap / 5
    winner.save()
    loser.save()
    # create Battle object storing info about the battle
    b = Battle(log = log)
    b.save()
    b.participants.add(winner)
    b.participants.add(loser)
    b.save()
    # updates players and robots involved, awards scrap to the winner and loser, creates a battle and returns it
    return b


def updateLog(attacker, defender, damage , health):
    if(damage > 0):
        return "\n %s attacked %s for %d damage. %s now has %d health left!" % (attacker.name, defender.name, damage, defender.name, 0 if health < 0 else health)
    else:
        return "\n %s dodged %s's attack. %s still has %d health!" % (defender.name, attacker.name, defender.name, 0 if health < 0 else health)




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

def get_scrap(num_bots,winner_scrap,loser_scrap):

    return  int(math.ceil(25 * math.log(num_bots + 1,1 + winner_scrap /  loser_scrap)))

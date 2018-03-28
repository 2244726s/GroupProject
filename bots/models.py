from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #currency of game
    scrap = models.IntegerField(default = 100)
    # tracks who the player is interested in, assymetrical since if you follow someone that doesn't mean they follow you
    follows = models.ManyToManyField("self", symmetrical = False)
    looking_for_match = models.BooleanField(default = False)
    # robot is in quotation marks because the class hasnt been defined yet
    # also, originally implemented with blank = True, but that doesn't seem to do what I think it did, so instead I used null = True and default = None
        # robot chosen for battle
    chosen_robot= models.OneToOneField("Robot", null= True, default = None)
    wins = models.IntegerField(default = 0)
    losses = models.IntegerField(default = 0)
    def __str__(self):
        return self.user.username

class Robot(models.Model):
    owner = models.ForeignKey(Player, on_delete = models.CASCADE)
    name = models.CharField(max_length = 20, unique = True)
    value = models.IntegerField() # scrap value of robot
    type = models.CharField(max_length = 10) # class of robot
    wins = models.IntegerField(default = 0)
    losses= models.IntegerField(default = 0)
    # robot stats
    speed = models.IntegerField(null = True, blank = True)
    dodge = models.IntegerField(null = True, blank = True)
    armour = models.IntegerField(null = True, blank = True)
    weapon = models.IntegerField(null = True, blank = True)
    accuracy = models.IntegerField(null = True, blank = True)
    # returns dictionary with names of stats mapped to corresponding values
    def get_stats(self):
        stats = {
            'speed' : self.speed,
            'dodge': self.dodge,
            'armour' : self.armour,
            'weapon' : self.weapon,
            'accuracy' : self.accuracy,
        }
        return stats

    def __str__(self):
        return self.name

class Battle(models.Model):
    participants = models.ManyToManyField(Player)
    log = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        result = ""
        for p in self.participants.all():
            if result == "":
                result  = str(p)
            else:
                result += ' vs ' + str(p)
        #end for
        date = self.date.strftime('%d/%m %H:%M')
        result += ', ' + date
        #result += ', ' + str(self.date)
        if self.log:
            result += ', ' + self.log.split('\n')[-1]
        else:
            result += ', pending'

        return result

class Team(models.Model):
    player = models.ForeignKey(Player)
    bots = models.ManyToManyField(Robot)
    num_bots = models.IntegerField(default = 1)


class Challenge(models.Model):
    challenger = models.OneToOneField(Team, related_name = 'challenger')
    challengee = models.ForeignKey(Team, related_name='challengee', null = True, blank = True, unique = False)
    num_bots = models.IntegerField(default = 1)
    date = models.DateField(auto_now_add = True)




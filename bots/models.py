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
    # insert robot stats fields once game mechanics become clear
    # planning on implementing it as a dictionary of stats
    #e.g stats["strength"] = models.IntegerField()
    speed = models.IntegerField()
    dodge = models.IntegerField()
    armour = models.IntegerField()
    weapon = models.IntegerField()
    accuracy = models.IntegerField()
    def __str__(self):
        return self.name

class Battle(models.Model):
    participants = models.ManyToManyField(Player)
    log = models.TextField()
    date = models.DateTimeField(auto_now_add = True)

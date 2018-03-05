from django.test import TestCase
from bots.models import *
from bots import mechanics
import basic_populate

# Create your tests here.

    # helper method 
def createPlayer():
    u = User(username='testuser', password="")
    u.save()
    p = Player(user=u)
    p.save()
    return p
def createRobot(owner):
    r = Robot(owner =owner, name='r2d2', type = mechanics.WHEELED, value = 10,speed = 10, armour =5, dodge =1, weapon =5,accuracy =10)
    return r

class ModelTests(TestCase):
    ''' tests for models.py'''
    

    
    def testCanCreatePlayer(self):
        p = createPlayer()

    def testCanCreateRobot(self):
        p = createPlayer()
        createRobot(p)
        
class MechanicsTests(TestCase):
    def testBattleFuncRuns(self):
# populate database    
        basic_populate.run()
        r1 = Robot.objects.all()[0]
        r2 = Robot.objects.all()[1]
        mechanics.battle(r1, r2)
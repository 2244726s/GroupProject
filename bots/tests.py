from django.test import TestCase
from bots.models import *
from bots import mechanics, matchmaking
import basic_populate

# Create your tests here.

    # helper method 
def createPlayer(p_id):
    u = User(username='testuser'+str(p_id), password="")
    u.save()
    p = Player(user=u)
    p.save()
    return p

def createRobot(owner, r_id):
    r = Robot(owner =owner, name='robot'+str(r_id), type = mechanics.WHEELED, value = 10,speed = 10, armour =5, dodge =1, weapon =5,accuracy =10)
    r.save()
    return r

class ModelTests(TestCase):
    ''' tests for models.py'''
    def testCanCreatePlayer(self):
        p = createPlayer(0)

    def testCanCreateRobot(self):
        p = createPlayer(0)
        createRobot(p,0)
        
class MechanicsTests(TestCase):
    def testBattleFuncRuns(self):
# populate database    
        basic_populate.run()
        r1 = Robot.objects.all()[0]
        r2 = Robot.objects.all()[1]
        b = mechanics.battle([r1], [r2])
        print(b.log)
    
    def testIfChallengeMatchesUpForBattle(self):
        p1 = createPlayer(0)
        p2 = createPlayer(1)
        r1=[]
        for i in range(0,3):
            r1 += [createRobot(p1,i)]
        r2=[]
        for i in range(3, 3+3):
            r2 += [createRobot(p2,i)]
        
        #count initial number of battles in DB
        n = len(Battle.objects.all())
        # issue initial challenge
        matchmaking.challenge(p1,p2,r1)
        # there shouldnt be any more battles yet
        self.assertEquals(len(Battle.objects.all()), n)
        
        #issue counter challenge
        matchmaking.challenge(p2, p1, r2)
        # now there should be a new battle in db
        self.assertEquals(len(Battle.objects.all()), n+1)

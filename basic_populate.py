'''very basic population script '''
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GroupProject.settings')
import django
django.setup()

from bots.models import *
from bots import mechanics

# create some players
u = User.objects.get_or_create(username='sam', password="")[0]
u.save()
p1 = Player.objects.get_or_create(user=u)[0]
p1.save()

u = User.objects.get_or_create(username='hannah', password="")[0]
u.save()
p2 = Player.objects.get_or_create(user=u)[0]
p2.save()

u = User.objects.get_or_create(username='jonathan', password="")[0]
u.save()
p3 = Player.objects.get_or_create(user=u)[0]
p3.save()


# make a robot for every player
r1 = Robot.objects.get_or_create(owner =p1, name='r2d2', type = mechanics.WHEELED, value = 10,speed = 10, armour =5, dodge =1, weapon =5,accuracy =10)[0]
r1.save()
r2 = Robot.objects.get_or_create(owner =p2, name='C3P0', type = mechanics.BIPEDAL, value = 10,speed = 5, armour =6, dodge =8, weapon =3,accuracy =5)[0]
r2.save()
mechanics.battle(r1,r2)
r1 = Robot.objects.get_or_create(owner =p3, name='HL2', type = mechanics.AERIAL, value = 10,speed = 20, armour =3, dodge =15, weapon =2,accuracy =5)[0]
r1.save()

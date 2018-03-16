from django.contrib import admin
from bots.models import Player, Robot, Battle, Team

# Register your models here.
admin.site.register(Player)
admin.site.register(Robot)
admin.site.register(Battle)
admin.site.register(Team)
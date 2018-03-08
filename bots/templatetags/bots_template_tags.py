from django import template
from bots .models import Robot

register = template.Library()

@register.inclusion_tag ('bots/bot_table.html')
def get_bot_table(robot):
    return {
        'robot' : robot,
        'stats' : robot.get_stats(),
        'player' : robot.owner,
    }

@register.filter(name='mult')
def mult(value, arg):
    return int(value) * int(arg)
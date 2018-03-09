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

@register.inclusion_tag('bots/partials/bot_stat_td.html')
def get_bot_stat(robot, stat):
    return {
        'robot' : robot,
        'value' : robot.get_stats()[stat],
        'stat' : stat,
    }
"""
script for populating database with valid sample data
"""
from random import shuffle, randint, choice

#create list of adjectives and animals to generate usernames for fake accounts
adjectives = ['Happy', 'Grumpy', 'Tipsy', 'Sleepy', 'Sneaky', 'Hungry', 'Pretty']
animals = ['Lion', 'Panda', 'Hippo', 'Zebra', 'Badger', 'Bee', 'Monkey']
# combine the two lists together to create list of user names
names = [y+x for x in animals for y in adjectives]
#shuffle list of names
shuffle(names)

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ'"
# list of the robot names for tracking uniqueness 
robot_names = []

def gen_bot_name():
    ''' returns unique robot__name'''
    name = choice(letters) + randint(0,10) + choice(letters) + randint(0,10)
    # check if unique
    if name not in robot_names:
        robot_names += name
        return name
    else: # name isnt unique
        return gen_bot_name()


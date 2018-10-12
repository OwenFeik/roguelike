from random import randint

def from_dungeon_floor(table,floor):
    for (value,level) in reversed(table):
        if floor >= level:
            return value
    
    return 0


def random_choice_index(chances):
    random_chance=randint(1,sum(chances))

    running_sum=0
    choice=0
    for w in chances:
        running_sum+=w

        if random_chance<=running_sum:
            return choice
        choice+=1

def random_choice_from_dict(source_dict):
    choices=list(source_dict.keys())
    chances=list(source_dict.values())

    return choices[random_choice_index(chances)]
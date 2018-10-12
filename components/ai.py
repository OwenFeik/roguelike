import libtcodpy as lc
from random import randint
from gamemessages import Message

class BasicMonster:
    def to_json(self):
        return {'ai':'BasicMonster'}

    def take_turn(self,target,fov_map,game_map,entities):
        results=[]
        
        enemy=self.owner
        if lc.map_is_in_fov(fov_map,enemy.x,enemy.y):
            if enemy.distance_to(target)>=2:
                enemy.move_astar(target,entities,game_map)
            elif target.fighter.health>0:
                attack_results=enemy.fighter.attack(target)
                results.extend(attack_results)
        
        return results

class ConfusedMonster:
    def to_json(self):
        json_data={
            'ai':'ConfusedMonster',
            'previous_ai':self.previous_ai.to_json(),
            'number_of_turns':self.number_of_turns
        }
        return json_data

    def __init__(self,previous_ai,number_of_turns):
        self.previous_ai=previous_ai
        self.number_of_turns=number_of_turns
    
    def take_turn(self,target,fov_map,game_map,entities):
        results=[]

        if self.number_of_turns>0:
            random_x=self.owner.x+randint(0,2)-1
            random_y=self.owner.y+randint(0,2)-1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x,random_y,game_map,entities)
            
            self.number_of_turns-=1
        else:
            self.owner.ai=self.previous_ai
            results.append({'message':Message('The {0} is no longer confused!'.format(self.owner.name),lc.red)})

        return results

def from_json(json_data):
    ai=globals()[json_data.get('ai')]
    if ai==BasicMonster:
        return BasicMonster()
    elif ai==ConfusedMonster:
        previous_ai=from_json(json_data.get('previous_ai'))
        number_of_turns=json_data.get('number_of_turns')
        return ConfusedMonster(previous_ai,number_of_turns)


# So, turns out globals() is a thing
# def create_ai_component(ai,**kwargs):
#     exec_output={}

#     if kwargs.get('previous_ai'):
#         previous_ai=kwargs.get('previous_ai')
#         del kwargs['previous_ai']
#         arg_string=''
#         for kwarg in kwargs:
#             arg_string+='{0}={1},'.format(kwarg,kwargs[kwarg])
#         arg_string=arg_string[:-1]
#         exec('from components.ai import {0},{1}\nprevious_ai_component={1}()\nai_component={0}(previous_ai=previous_ai_component,{2})'.format(ai,previous_ai,arg_string),exec_output)
#     else:
#         arg_string=''
#         for kwarg in kwargs:
#             arg_string+='{0}={1},'.format(kwarg,kwargs[kwarg])
#         arg_string=arg_string[:-1]
#         exec('from components.ai import {0}\nai_component={0}({1})'.format(ai,arg_string),exec_output)

#     return exec_output['ai_component']